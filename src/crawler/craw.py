from crawler.requester  import *
from crawler.exceptions import *
from crawler.crawparser import *
from crawler.validator  import *


# Functions that fetch all Departments from the system
def fetch_departments():
    print('[Work] Fetching departments ......')
    url = 'https://cis.ncu.edu.tw/Course/main/query/byUnion'
    reqter = Requester()
    response = reqter.getter(url)
    
    en_result = None
    ch_result = None
    # First try to get the response from the server
    if response is None:
        print('Get null response from the server at fetch_departments() (1/2)')
        print('[Fatel error] Departments not fetched')
        raise NullResponseError
    
    if reqter.is_english():
        reqter.toggle_language()
        response = reqter.getter(url)
        if response is None:
            print('Get null response from the server at fetch_departments() (1/2)')
            print('[Fatel error] Departments not fetched')
            raise NullResponseError
        
    print('Parsing Chinese department data ......')
    ch_facility, ch_result = parse_department(response)
    
    reqter.toggle_language()
    response = reqter.getter(url)
    if response is None:
        print('Get null response from the server at fetch_departments() (2/2)')
        print('[Fatel error] Departments not fetched')
        raise NullResponseError
    
    print('Parsing Chinese department data ......')
    en_facility, en_result = parse_department(response)
        
    validated = val_departmrnts(en_result, ch_result)
    print('[Done] All departments fetched ......')
    
    return [{'name':{'en':en_facility[i]['name'],
                    'ch':ch_facility[i]['name'],},
                   'serial':en_facility[i]['serial'] } for i in range(len(en_facility))],[
            {'name':{'en':en_result[i]['name'],
                     'ch':ch_result[i]['name']},
             'facility': en_result[i]['facility_ser'],
             'url'    : en_result[i]['url'],
             'course_cnt': en_result[i]['course_cnt']} for i in range(len(en_result))]
