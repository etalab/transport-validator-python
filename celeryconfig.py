import os

broker_url = os.environ.get('RABBITMQ_URL', 'amqp://localhost')
result_backend = os.environ.get('MONGODB_URL', 'mongodb://localhost/transport')
result_persitent = True
