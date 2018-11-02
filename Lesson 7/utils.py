from wit import Wit
from gnewsclient import gnewsclient

access_token = "VE64C2OZJDQHNXAAOA3T2A6R2BDWPP54"

client = Wit(access_token=access_token)


def wit_response(message_text):
    resp = client.message(message_text)
    categories = {'newstype': None, 'location': None}

    entities = list(resp['entities'])
    for entity in entities:
        categories[entity] = resp['entities'][entity][0]['value']

    return categories


def get_news_elements(categories):
    news_client = gnewsclient()
    news_client.query = ''

    if categories['newstype'] != None:
        news_client.query += categories['newstype'] + ' ' # for print result here will be a space

    if categories['location'] != None:
        news_client.query += categories['location']

    return news_client.query


print(get_news_elements(wit_response("I want sports news from india")))
