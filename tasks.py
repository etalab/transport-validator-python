import requests, tempfile, os, transitfeed
from io import BytesIO
from transport_validator.validator import Accumulator
from celery import Celery, states

app = Celery('tasks')
app.config_from_object('celeryconfig')
for envvar in ['CELERY_BROKER', 'CELERY_RESULT_BACKEND']:
    if envvar in os.environ:
        app.config_from_envvar(envvar)

if 'MONGODB_HOST' in os.environ:
    app.conf['CELERY_MONGODB_BACKEND_SETTINGS']['host'] = os.environ['MONGODB_HOST']

if 'MONGODB_USER' in os.environ:
    app.conf['CELERY_MONGODB_BACKEND_SETTINGS']['user'] = os.environ['MONGODB_USER']

if 'MONGODB_PASSWORD' in os.environ:
    app.conf['CELERY_MONGODB_BACKEND_SETTINGS']['password'] = os.environ['MONGODB_PASSWORD']

if 'MONGODB_DATABASE' in os.environ:
    app.conf['CELERY_MONGODB_BACKEND_SETTINGS']['database'] = os.environ['MONGODB_DATABASE']

if 'MONGODB_PORT' in os.environ:
    app.conf['CELERY_MONGODB_BACKEND_SETTINGS']['port'] = os.environ['MONGODB_PORT']

@app.task(bind=True)
def perform(self, url):
#Download the file
    r = requests.get(url)
    self.update_state(state='DOWNLOADED')
    if r.status_code != 200:
        raise Exception("Bad status code {} {}".format(url, r.status_code))

#Save it in a temp file
    d = tempfile.mkdtemp()
    filename = os.path.join(d, "gtfs.zip")
    with open(filename, "wb") as f:
        f.write(r.content)

#Load it
    accumulator = Accumulator()
    problems = transitfeed.ProblemReporter(accumulator)
    gtfs_factory = transitfeed.GetGtfsFactory()
    loader = gtfs_factory.Loader(filename, problems=problems,
                                 extra_validation=False,
                                 gtfs_factory=gtfs_factory)
    schedule = loader.Load() #this is a transport schedule
    self.update_state(state='LOADED')
#Remove tempfiles
    os.remove(filename)
    os.rmdir(d)

#Run validation & return results
    schedule.Validate(validate_children=False)
    self.update_state(state=states.SUCCESS)
    accumulator = problems.GetAccumulator()
    return {
        "validations":
        {key: [value.GetDictToFormat() for value in getattr(accumulator, key)]
         for key in ["errors", "warnings", "notices"]}
    }
