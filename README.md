Transport validator
===================

Requirements
-------------
 * Python 2.7
 * Rabbitmq
 * Mongodb

Setup
-----

Make a virtualenv and run `pip install -r requiremnts.txt`

Configuration
-------------

You can modify the configuration in celeryconfig.py

Run
---

Run with : `celery -A tasks worker`
