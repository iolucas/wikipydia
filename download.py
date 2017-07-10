import requests
from . import exceptions
from url import URL

#PageRequestTimeout = exceptions.PageRequestTimeout
#PageDoesNotExists = exceptions.PageDoesNotExists

#from exceptions import PageRequestTimeout, PageDoesNotExists

def _download_page_data(page, lang, timeout):
    """Function to retrieve a wikipedia page in html form, with its sections"""
    #import exceptions

    assert isinstance(page, URL)

    # https://en.wikipedia.org/w/api.php?action=parse&redirects&page=fluid_mechanics

    req_params = [
        'action=parse',
        'redirects',
        'format=json',
        'prop=text|displaytitle',
        'page=' + page.quoted
    ]

    wikipedia_api_url = "https://" + lang + ".wikipedia.org/w/api.php?" + "&".join(req_params)

    try:
        page_data = requests.get(wikipedia_api_url, timeout=timeout).json()
    except requests.exceptions.ConnectTimeout:
        raise exceptions.PageRequestTimeout(page, lang, timeout)

    #If the object parse is not in the json object, page does not exists
    if not 'parse' in page_data:
        raise exceptions.PageDoesNotExists(page, lang)

    page_title = page_data['parse']['title']
    page_id = page_data['parse']['pageid']
    page_html = page_data['parse']['text']['*']

    return page, page_title, page_id, page_html


def _download_langlinks(title, lang, timeout):
    """Function to retrieve links to pages of the same content but other languages."""
    
    #https://www.mediawiki.org/wiki/API:Langlinks
    #https://en.wikipedia.org/w/api.php?action=query&titles=Technical_drawing&prop=langlinks&lllimit=500

    assert isinstance(title, URL)

    req_params = [
        'action=query',
        'format=json',
        'prop=langlinks',
        'lllimit=500',
        'llprop=url',
        'titles=' + title.quoted
    ]

    wikipedia_api_url = "https://" + lang + ".wikipedia.org/w/api.php?" + "&".join(req_params)

    #try:
    page_data = requests.get(wikipedia_api_url, timeout=timeout).json()
    #except requests.exceptions.ConnectTimeout:
        #raise exceptions.PageRequestTimeout(page, lang, timeout)

    langlinks = list()
        
    for pageid, pagedata in page_data['query']['pages'].items():
        if pageid == "-1":
            raise Exception("Page does not exists.")
        
        if 'langlinks' not in pagedata:
            continue
            
        for link in pagedata['langlinks']:
            url_offset = link['url'].find("/wiki/")
            if url_offset == -1:
                link_url = None
            else:
                link_url = link['url'][url_offset+6:]

            langlinks.append((link["lang"], link["*"], link_url))
            
    return langlinks
