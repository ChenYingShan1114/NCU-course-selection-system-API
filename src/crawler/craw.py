from crawler.requester  import *
from crawler.exceptions import *
from crawler.crawparser import *

# Functions that fetch all Departments from the system
def fetch_departments():
    print('[Work] Fetching departments ......')
    url = 'https://cis.ncu.edu.tw/Course/main/query/byUnion'
    reqter = Requester()
    response = reqter.getter(url)
    en_result = None
    ch_result = None
    # First try to get the response from the server
    if response is not None:
        first_is_english = is_english(response)
    else:
        print('Get null response from the server at fetch_departments() (1/2)')
        print('[Fatel error] Departments not fetched')
        raise NullResponseError

    if first_is_english:
        print('Parsing English department data ......')
        en_result = parse_department(response)
    else :
        print('Parsing Chinese department data ......')
        ch_result = parse_department(response)
    
    # Second try to get the response from the server (toggled language)
    reqter.toggle_language()
    response = reqter.getter(url)
    if response is not None:
        if first_is_english:
            print('Parsing English department data ......')
            ch_result = parse_department(response)
        else :
            print('Parsing Chinese department data ......')
            en_result = parse_department(response)
    else:
        print('Get null response from the server at fetch_departments() (2/2)')
        print('[Fatel error] Departments not fetched')
        raise NullResponseError
    
    # Cross check if the two results are the same
    if len(en_result) != len(ch_result):
        print('[Fatel error] English and Chinese department data mismatched')
        print('[Fatel error] English and Chinese department data mismatched')
        print('==================[Length mismatch]==================')
        print('Length of English result: ' + str(len(en_result)))
        print('Length of Chinese result: ' + str(len(ch_result)))
        raise ChEnDataMismatchError
    result = []
    for i in range(len(en_result)):
        if en_result[i]['url'] != ch_result[i]['url']:
            
            raise ChEnDataMismatchError
        if en_result[i]['courses'] != ch_result[i]['courses']:
            print('[Fatel error] English and Chinese department data mismatched')
            print('===================[Data mismatch]===================')
            print('Mismatched data at index: ' + str(i))
            print('En: ' + str(en_result[i]))
            print('Ch: ' + str(ch_result[i]))
            raise ChEnDataMismatchError
        else:
            result.append({
                'en'     : en_result[i]['name'],
                'ch'     : ch_result[i]['name'],
                'url'    : en_result[i]['url'],
                'courses': en_result[i]['courses'],
            })
    return result 