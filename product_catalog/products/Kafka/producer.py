import json
from confluent_kafka import Producer

def produce_cpe_message(cpe_name):
    producer = Producer({
        'bootstrap.servers': 'localhost:9092'
    })

    message = {
        'cpe_name': cpe_name
    }
    print(message)

    producer.produce('cpe_topic', key=cpe_name, value=json.dumps(message))
    producer.flush()
