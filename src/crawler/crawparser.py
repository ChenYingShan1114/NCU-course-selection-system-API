from bs4 import BeautifulSoup as bs
import re
from crawler.exceptions import RegEXNullMatchesErr



# Function that parses the department page and returns a dictionary,
# containing the department name, url to the department contained course page 
# and the total number of courses in the department
def parse_department(response):
    html = bs(response.text, 'html.parser')
    main_tb = html.find_all('table',id='byUnion_table')[0]
    tables = main_tb.find_all('table')[1:]
    facilities = []
    results    = []
    for table in tables:
        facility = list(table.find_all('th')[0].stripped_strings)[0].strip()
        facilities.append(facility)
        items = table.find_all('li')
        for item in items:
            dep_url = 'https://cis.ncu.edu.tw' + item.a.get("href")
            dep_info_text = item.a.text.strip()
            matches = re.findall('\((.*?)\)', dep_info_text)
            try:
                if matches is None:
                    raise RegEXNullMatchesErr
                dep_course_cnt = int(matches[-1])
                dep_name = re.sub(f'\({dep_course_cnt}\)', '', dep_info_text)
            except RegEXNullMatchesErr as err:
                print('[Warning] Failed to extract total course info from department data : ' + dep_info_text)
                dep_course_cnt = 'N/A'
                dep_name = dep_info_text
            except ValueError as err:
                print('[Warning] Failed to convert total course info to int : ' + dep_info_text)
                dep_course_cnt = 'N/A'
                dep_name = dep_info_text

            results.append({
                'name'   : dep_name,
                'url'    : dep_url,
                'course_cnt': dep_course_cnt,
                'facility_ser': len(facilities)-1
            })
    return [{"name"   :facilities[index],
             "serial" :index} 
            for index in range(len(facilities))] , results


