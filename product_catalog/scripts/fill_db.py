import re
import requests
from bs4 import BeautifulSoup
from products.models import Product
from products.enums import Category

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
                        cpe_version = cpe_parts[1]
                        part = cpe_parts[2] # a => application, h => hardware, o => operating systems [part refers to cpe_type]
                        vendor = cpe_parts[3]
                        product = cpe_parts[4]
                        version = cpe_parts[5]
                        update = cpe_parts[6]
                        edition = cpe_parts[7]
                        language = cpe_parts[8]
                        sw_edition = cpe_parts[9]
                        target_sw = cpe_parts[10]
                        target_hw = cpe_parts[11]
                        other = cpe_parts[12]

                        category = Category.APPLICATION.value if part=='a' else Category.HARDWARE.value if part=="h" else Category.OS.value
						
                        cpe_detail = {'name':product, 'vendor':vendor, 'category':category, 'version':version, 'cpe_name':tagContent, 'website':cpe_url}

                        Product.objects.create(**cpe_detail)
                else:
                    break
				
                print(f"{current_index = }")
			# l'index s'incrémente par bond de 20
            current_index += 20
