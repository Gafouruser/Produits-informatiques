import requests

cpe_name = "cpe:2.3:a:adobe:flash_player_for_linux:9.0.31:*:*:*:*:*:*:*"

nvd_api = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={cpe_name}"

session = requests.Session()

nvd_api_response = session.get(nvd_api).json()

resultsPerPage = nvd_api_response['resultsPerPage']
startIndex = nvd_api_response['startIndex']
totalResults = nvd_api_response['totalResults']
vulnerabilities = nvd_api_response['vulnerabilities']

targeted_cve_list = set()

for aVulnDetail in vulnerabilities:
    cve_section = aVulnDetail['cve']

    cve_id = cve_section['id']
    cve_source = cve_section['sourceIdentifier']
    cve_released_date = cve_section['published']
    cve_updated_date = cve_section['lastModified']
    cve_vuln_status = cve_section['vulnStatus']
    cve_english_description = [language['value'] for language in cve_section['descriptions'] if language['lang']=='en'][0]
    cve_metrics = cve_section['metrics']
    """ # There is an example :
    'metrics': {'cvssMetricV2': [{'source': 'nvd@nist.gov', 'type': 'Primary', 
                'cvssData': {'version': '2.0', 'vectorString': 'AV:N/AC:M/Au:N/C:N/I:P/A:P', 'accessVector': 'NETWORK', 
                'accessComplexity': 'MEDIUM', 'authentication': 'NONE', 'confidentialityImpact': 'NONE', 
                'integrityImpact': 'PARTIAL', 'availabilityImpact': 'PARTIAL', 'baseScore': 5.8}, 'baseSeverity': 'MEDIUM', 
                'exploitabilityScore': 8.6, 'impactScore': 4.9, 'acInsufInfo': False, 'obtainAllPrivilege': False, 
                'obtainUserPrivilege': False, 'obtainOtherPrivilege': False, 'userInteractionRequired': True}]}
        Useful information can be extracted from that
    """
    cve_references = cve_section['references']
    """ # Here is an example...
    'references': [{'url': 'http://isc.sans.org/diary.html?storyid=5929', 'source': 'cve@mitre.org'}, 
    {'url': 'http://lists.apple.com/archives/security-announce/2009/May/msg00002.html', 'source': 'cve@mitre.org'}, 
    {'url': 'http://secunia.com/advisories/34226', 'source': 'cve@mitre.org'}, 
    {'url': 'http://secunia.com/advisories/34293', 'source': 'cve@mitre.org'}, 
    {'url': 'http://secunia.com/advisories/35074', 'source': 'cve@mitre.org'}, 
    {'url': 'http://security.gentoo.org/glsa/glsa-200903-23.xml', 'source': 'cve@mitre.org'}, 
    {'url': 'http://securitytracker.com/id?1021751', 'source': 'cve@mitre.org'}, 
    {'url': 'http://sunsolve.sun.com/search/document.do?assetkey=1-66-254909-1', 'source': 'cve@mitre.org'}, 
    {'url': 'http://support.apple.com/kb/HT3549', 'source': 'cve@mitre.org'}, 
    {'url': 'http://www.adobe.com/support/security/bulletins/apsb09-01.html', 'source': 'cve@mitre.org', 'tags': ['Patch', 'Vendor Advisory']},
    {'url': 'http://www.us-cert.gov/cas/techalerts/TA09-133A.html', 'source': 'cve@mitre.org', 'tags': ['US Government Resource']}, 
    {'url': 'http://www.vupen.com/english/advisories/2009/0513', 'source': 'cve@mitre.org', 'tags': ['Patch']}, 
    {'url': 'http://www.vupen.com/english/advisories/2009/0743', 'source': 'cve@mitre.org'}, 
    {'url': 'http://www.vupen.com/english/advisories/2009/1297', 'source': 'cve@mitre.org'}, 
    {'url': 'https://exchange.xforce.ibmcloud.com/vulnerabilities/48902', 'source': 'cve@mitre.org'}, 
    {'url': 'https://oval.cisecurity.org/repository/search/definition/oval%3Aorg.mitre.oval%3Adef%3A16419', 'source': 'cve@mitre.org'}, 
    {'url': 'https://oval.cisecurity.org/repository/search/definition/oval%3Aorg.mitre.oval%3Adef%3A6662', 'source': 'cve@mitre.org'}]}}
    """

    targeted_cve_list.add(cve_id)

    # there is a field named cpeMatch which informs about related cpe affected by the specific cve_id

print(targeted_cve_list)

session.close()