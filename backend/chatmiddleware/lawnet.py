import requests
from xml.etree import ElementTree

# COMMENTED OUT FOR SALNET API LICENSE USAGE
# BASE_URL = #
# SEARCH_URL = #
# CASE_URL = #
# HEADERS = #
# BODY = #


def search(search_string, headers=HEADERS, body=BODY, url=BASE_URL+SEARCH_URL):
    """ performs search on salnet api given search string, xml tree response """
    body['searchTerm'] = search_string
    response = requests.post(url, body, headers=headers)
    return(ElementTree.fromstring(response.content))


def retrieve_case(document_id, headers=HEADERS, body=BODY, url=BASE_URL+CASE_URL):
    """ retrieves case from salnet api given id, xml tree response """
    body['docUrl'] = document_id
    response = requests.post(url, body, headers=headers)
    return(ElementTree.fromstring(response.content))

