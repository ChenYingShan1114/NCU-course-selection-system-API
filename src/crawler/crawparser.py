from bs4 import BeautifulSoup as bs
import re
from crawler.exceptions import RegEXNullMatchesErr

weekdays_to_num_ch = {
    "一":1,
    "二":2,
    "三":3,
    "四":4,
    "五":5,
    "六":6,
    "日":7,
}

weekdays_to_num_en = {
    "Mon":1,
    "Tue":2,
    "Wed":3,
    "Thu":4,
    "Fri":5,
    "Sat":6,
    "Sun":7,
}

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


def parse_page_links(response):
    html = bs(response.text, 'html.parser')
    links = html.find_all('div',class_='pagelinks')
    if len(links) == 0:
        return []
    else:
        return ['https://cis.ncu.edu.tw'+a.get('href') for a in links[0].find_all('a')]
    
def parse_course_ch(response):
    html = bs(response.text, 'html.parser')
    main_tb = html.find_all('table',id='item')[0].find_all('tbody')[0]
    courses = main_tb.find_all('tr')
    results = []
    for course in courses:
        items = course.find_all('td')
        temp = list(items[0].stripped_strings)
        crs_serial = temp[0].strip()
        temp = temp[1].split("-")
        crs_code   = temp[0].strip()
        crs_class  = temp[1].strip()
        temp = list(items[1].stripped_strings)
        crs_name   = temp[0].strip()
        notice     = list(items[1].find_all('span',class_="notice"))
        if len(notice) == 0:
            crs_notice = ""
        else:
            crs_notice = notice[0].text.strip()
        crs_instructor = list(items[2].stripped_strings)
        crs_credits    = int(items[3].text.strip())
        crs_time_loc   = []        
        temp = list(items[4].stripped_strings)
        for data in temp:
            tmp = data.split(" ")
            time,loc = tmp[0].split("/")
            loc = loc.split("-")
            crs_time_loc.append({
                'time':{'week':weekdays_to_num_ch[time[0]],'session':list(time[1:])},
                'loc' :{'building':loc[0],'room':"-".join(loc[1:])},
            })
        crs_isRequired = items[5].text.strip() == "必修"
        crs_isFullSem  = items[6].text.strip() == "全"
        if items[7].text.strip() == "無":
            crs_MaxStu = -1
        else:
            crs_MaxStu     = int(items[7].text.strip())

        results.append({
            'serial'   : crs_serial,
            'code'     : crs_code,
            'class'    : crs_class,
            'name'     : crs_name,
            'notice'   : crs_notice,
            'instructor':crs_instructor,
            'credits'  : crs_credits,
            'time_loc' : crs_time_loc,
            'isRequired':crs_isRequired,
            'isFullSem':crs_isFullSem,
            'MaxStu'   :crs_MaxStu,
        })
    return results

def parse_course_en(response):
    html = bs(response.text, 'html.parser')
    main_tb = html.find_all('table',id='item')[0].find_all('tbody')[0]
    courses = main_tb.find_all('tr')
    results = []
    for course in courses:
        items = course.find_all('td')
        temp = list(items[0].stripped_strings)
        crs_serial = temp[0].strip()
        temp = temp[1].split("-")
        crs_code   = temp[0].strip()
        crs_class  = temp[1].strip()
        temp = list(items[1].stripped_strings)
        crs_name   = temp[0].strip()
        notice     = list(items[1].find_all('span',class_="notice"))
        if len(notice) == 0:
            crs_notice = ""
        else:
            crs_notice = notice[0].text.strip()
        crs_instructor = list(items[2].stripped_strings)
        crs_credits    = int(items[3].text.strip())
        crs_time_loc   = []        
        temp = list(items[4].stripped_strings)
        for data in temp:
            tmp = data.split(" ")
            time,loc = tmp[0].split("/")
            loc = loc.split("-")
            crs_time_loc.append({
                'time':{'week':weekdays_to_num_en[time[:3]],'session':list(time[3:])},
                'loc' :{'building':loc[0],'room':"-".join(loc[1:])},
            })
        crs_isRequired = items[5].text.strip() == "Required"
        crs_isFullSem  = items[6].text.strip() == "Whole Year"
        if items[7].text.strip() == "Unlimited":
            crs_MaxStu = -1
        else:
            crs_MaxStu     = int(items[7].text.strip())

        results.append({
            'serial'   : crs_serial,
            'code'     : crs_code,
            'class'    : crs_class,
            'name'     : crs_name,
            'notice'   : crs_notice,
            'instructor':crs_instructor,
            'credits'  : crs_credits,
            'time_loc' : crs_time_loc,
            'isRequired':crs_isRequired,
            'isFullSem':crs_isFullSem,
            'MaxStu'   :crs_MaxStu,
        })
    return results