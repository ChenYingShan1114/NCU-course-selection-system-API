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
    
    if reqter.is_english():
        reqter.toggle_language()
        response = reqter.getter(url)
        
    print('Parsing Chinese department data ......')
    ch_facility, ch_result = parse_department(response)
    
    reqter.toggle_language()
    response = reqter.getter(url)
    
    print('Parsing Chinese department data ......')
    en_facility, en_result = parse_department(response)
        
    validated = val_departmrnts(en_result, ch_result)
    print('[Done] All departments fetched ......')
    
    return [{'name':{'en':en_facility[i]['name'],
                    'ch':ch_facility[i]['name'],},
                   'serial':en_facility[i]['serial'] } for i in range(len(en_facility))],[
            {'name':{'en':en_result[i]['name'],
                     'ch':ch_result[i]['name']},
             'facility_ser': en_result[i]['facility_ser'],
             'department_serial': i,
             'url'         : en_result[i]['url'],
             'course_cnt'  : en_result[i]['course_cnt']} for i in range(len(en_result))]

# Function that fetches all courses from the given department
def fetch_courses(department_data):
    deparement_url = department_data['url']
    print('[Work] Fetching departments ......')
    reqter = Requester()
    response = reqter.getter(deparement_url)

    en_result = []
    ch_result = []
    
    if reqter.is_english():
        reqter.toggle_language()
        response = reqter.getter(deparement_url)

    page_links = [deparement_url] + parse_page_links(response)
    print(f'Found {len(page_links)} pages of courses ......')
    
    print('Parsing Chinese course data ......')
    for page_index in range(len(page_links)):
        response = reqter.getter(page_links[page_index])
        ch_result += parse_course_ch(response)

    reqter.toggle_language()
    
    print('Parsing English course data ......')
    for page_index in range(len(page_links)):
        response = reqter.getter(page_links[page_index])
        en_result += parse_course_en(response)
    
    validated = val_course_info(en_result, ch_result)
    print('[Done] All departments fetched ......')
    
    return [{'serial'    : en_result[i]['serial'], 
            'department_serial': department_data['department_serial'],
            'code'       : en_result[i]['code'],
            'class'      : en_result[i]['class'],
            'name'       : {'en':en_result[i]['name'],
                            'ch':ch_result[i]['name']},
            'notice'     : {'en':en_result[i]['notice'],
                            'ch':ch_result[i]['notice']},
            'instructor' : {'en':en_result[i]['instructor'],
                            'ch':ch_result[i]['instructor']},
            'credits'    : en_result[i]['credits'],
            'time_loc'   : en_result[i]['time_loc'],
            'isRequired' : en_result[i]['isRequired'],
            'isFullSem'  : en_result[i]['isFullSem'],
            'MaxStu'     : en_result[i]['MaxStu']
             } for i in range(len(en_result))]