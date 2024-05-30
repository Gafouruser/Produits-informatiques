import os
import django
import json
import requests, sys
from confluent_kafka import Consumer, KafkaException


# Configuration de l'environnement Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "product_catalog.settings")
django.setup()


# Import des modèles Django
from products.models import Vulnerability, Product

def fetch_cves_from_nvd(cpe_name):
    nvd_api = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={cpe_name}"
    response = requests.get(nvd_api, headers={'apiKey': "05f2d608-636e-4984-afc3-e7bb786de8f1" })
    print(response.status_code)
    if response.status_code == 200:
        print(response.json())
        data = response.json()
        print(f"Fetched CVEs from NVD for CPE Name: {cpe_name}")
        return data.get('vulnerabilities', [])
    else:
        print(f"Failed to fetch CVEs from NVD for CPE Name: {cpe_name}")
        return []

def process_message(message):
    cve_data = json.loads(message.value().decode('utf-8'))
    cpe_name = cve_data['cpe_name']
    print(f"Processing message for CPE Name: {cpe_name}")

    print("bob1")
    cves = fetch_cves_from_nvd(cpe_name)
    print(cves)

    for cve in cves:
        cve_section = cve['cve']
        cve_id = cve_section['id']
        description = [language['value'] for language in cve_section['descriptions'] if language['lang']=='en'][0]
        products = Product.objects.filter(cpe_name=cpe_name)

        for product in products:
            Vulnerability.objects.update_or_create(
                name=cve_id,
                defaults={
                    'description': description,
                    'product': product
                }
            )
            print(f"Stored CVE: {cve_id} for Product: {product.cpe_name}")

def main():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['cpe_topic'])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code():
                    raise KafkaException(msg.error())
            process_message(msg)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
    main()
