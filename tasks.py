import requests, tempfile, os, transitfeed
from io import BytesIO
from transport_validator.validator import Accumulator
from celery import Celery, states

app = Celery('tasks')
app.config_from_object('celeryconfig')

@app.task(bind=True)
def perform(self, url):
    r = requests.get(url)
    self.update_state(state='DOWNLOADED')
    if r.status_code != 200:
        raise Exception("Bad status code {} {}".format(url, r.status_code))
    d = tempfile.mkdtemp()
    filename = os.path.join(d, "gtfs.zip")
    with open(filename, "wb") as f:
        f.write(r.content)
    accumulator = Accumulator()
    problems = transitfeed.ProblemReporter(accumulator)
    gtfs_factory = transitfeed.GetGtfsFactory()
    loader = gtfs_factory.Loader(filename, problems=problems,
                                 extra_validation=False,
                                 gtfs_factory=gtfs_factory)
    schedule = loader.Load()
    self.update_state(state='LOADED')
    os.remove(filename)
    os.rmdir(d)

    schedule.Validate(validate_children=False)
    self.update_state(state=states.SUCCESS)
    accumulator = problems.GetAccumulator()
    return {
        "validations":
        {key: [value.GetDictToFormat() for value in getattr(accumulator, key)]
         for key in ["errors", "warnings", "notices"]}
    }
