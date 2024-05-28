import re
import requests
from bs4 import BeautifulSoup
from products.models import Product, Vulnerability
from products.enums import Category
from concurrent.futures import ThreadPoolExecutor

def run():
    # keyword a une taille comprise entre 3 et 512 caractères
    keywords = ['linux', 'windows']

    for keyword in keywords:
        current_index = 0
        
        while True:
            conn = requests.get(f"https://nvd.nist.gov/products/cpe/search/results?namingFormat=2.3&orderBy=CPEURI&keyword={keyword}&status=FINAL&startIndex={current_index}")

            if conn.status_code == 200:
                soup = BeautifulSoup(conn.text, 'html.parser')

                pattern = re.compile(r'^cpe:*')
						
                anchor_tags = soup.find_all('a', string=pattern)

                if anchor_tags:
                    for tag in anchor_tags :
                        tagContent = tag.text.strip()
                        cpe_parts = tagContent.split(":")
                        cpe_url = "https://nvd.nist.gov" + tag.get('href')
                        """ #This is the format of a CPE...
						cpe:<cpe_version>:<part>:<vendor>:<product>:<version>:<update>:<edition>:<language>:<sw_edition>:<target_sw>:<target_hw>:<other>
						"""
                        part = cpe_parts[2] # a => application, h => hardware, o => operating systems [part refers to cpe_type]
                        vendor = cpe_parts[3]
                        product = cpe_parts[4]
                        version = cpe_parts[5]

                        category = Category.APPLICATION.value if part=='a' else Category.HARDWARE.value if part=="h" else Category.OS.value
						
                        cpe_detail = {'name':product, 'vendor':vendor, 'category':category, 'version':version, 'cpe_name':tagContent, 'website':cpe_url}

                        product_instance = Product.objects.create(**cpe_detail)
                        retrieveCVEsPerCPE_(product_instance, tagContent, product)
                else:
                    break
				
                print(f"{current_index = }")
			# l'index s'incrémente par bond de 20
            current_index += 20


def retrieveCVEsPerCPE_(product_object, product_cpe_name, product_name):    
    nvd_api = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={product_cpe_name}"

    session = requests.Session()
    nvd_api_response = session.get(nvd_api).text
    if nvd_api_response:
        nvd_api_response = nvd_api_response.json()
        vulnerabilities = nvd_api_response['vulnerabilities']

        for aVulnDetail in vulnerabilities:
            cve_section = aVulnDetail['cve']
            cve_id = cve_section['id']
            cve_english_description = [language['value'] for language in cve_section['descriptions'] if language['lang']=='en'][0]
            product_object.vulnerabilities.add(Vulnerability.objects.get_or_create(name=cve_id, description=cve_english_description)[0])
        print("     CVEs added....")
    session.close()
