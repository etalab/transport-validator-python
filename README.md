Transport validator
===================

Requirements
-------------
 * Python 2.7
 * Rabbitmq
 * Mongodb

Setup
-----

 * Install virtualenv:
`pip install --user virtualenvwrapper`

 * Source it:
`source /usr/local/bin/virtualenvwrapper.sh`

 * Make a virtualenv:
`mkvirtualenv datavalidator`

 * Install dependencies
`pip install -r requiremnts.txt`

You might have have to activate the virtualenv with:

`workon datavalidator`

Configuration
-------------

You can modify the configuration in celeryconfig.py

Run
---

Run with : `celery -A tasks worker`
