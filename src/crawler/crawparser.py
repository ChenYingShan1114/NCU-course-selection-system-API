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

def parse_course_detail_ch(response):
    html = bs(response.text, 'html.parser')
    tables = html.find_all('table',class_='classBase')
    rows = tables[0].find_all('tr')
    crs_dept   = rows[4].find_all('td')[1].text.strip()
    crs_system = rows[5].find_all('td')[1].text.strip()
    crs_lang   = rows[10].find_all('td')[1].text.strip()
    crs_card   = rows[11].find_all('td')[1].text.strip()
    crs_assigned = int(rows[13].find_all('td')[1].text.strip())
    crs_selected = int(rows[14].find_all('td')[1].text.strip())

    crs_remark   = "\n".join(list(rows[15].find_all('td')[1].stripped_strings))
    crs_remark = re.sub(r'[\r\t]','',crs_remark)
    crs_goal     = "\n".join(list(rows[16].find_all('td')[1].stripped_strings))
    crs_goal = re.sub(r'[\r\t]','',crs_goal)
    crs_outline  = "\n".join(list(rows[17].find_all('td')[1].stripped_strings))
    crs_outline = re.sub(r'[\r\t]','',crs_outline)
    crs_textbook = "\n".join(list(rows[18].find_all('td')[1].stripped_strings))
    crs_textbook = re.sub(r'[\r\t]','',crs_textbook)

    crs_selfCompiledRate = rows[19].find_all('td')[1].text.strip()
    crs_instructMethod   = rows[20].find_all('td')[1].text.strip()
    crs_instructMethod = re.sub(r'[\r\t]','',crs_instructMethod)


    crs_gradMethod       = "\n".join(list(rows[21].find_all('td')[1].stripped_strings))
    crs_gradMethod = re.sub(r'[\r\t]','',crs_gradMethod)
    crs_officeHour       = "\n".join(list(rows[22].find_all('td')[1].stripped_strings))
    crs_officeHour = re.sub(r'[\r\t]','',crs_officeHour)

    crs_teachWeeks       = rows[23].find_all('td')[1].text.strip()
    
    crs_flexDiscription  = "\n".join(list(rows[24].find_all('td')[1].stripped_strings))
    crs_flexDiscription = re.sub(r'[\r\t]','',crs_flexDiscription)

    crs_domain           = "\n".join(list(rows[25].find_all('td')[1].stripped_strings))
    crs_domain           = re.sub(r'[\r\t]','',crs_domain)

    temp = html.find_all('table',class_='courseMap')[0].find_all('tr')
    csr_map = []
    if len(temp) > 1:
        for tmp in temp[2:]:
            tmp = tmp.find_all('td') 
            csr_map.append({
                'competencies' :tmp[0].text.strip(),
                'rating'       :re.sub(r'\s+','',tmp[1].text.strip()),
                'assesments'   :[i.strip() for i in tmp[2].text.strip().split("，")],
            })
    temp = html.find_all('table',id='AutoNumber1')
    crs_assignCriteria = []
    if len(temp) != 0:
        temp = temp[0].find_all('tr')
        for tmp in temp[1:]:
            tmp = tmp.find_all('td')
            crs_assignCriteria.append(tmp[1].text.strip())
    
    temp = html.find_all('table',id='std')
    crs_preselecStu = 0
    crs_stuGender = {'male':0,'Female':0}
    crs_stuGrade  = {'doctor':{},'master':{},'bachelor':{}}
    crs_stus = []
    if len(temp) != 0:
        temp = temp[0].find_all('tr')
        for tmp in temp[1:]:
            tmp = tmp.find_all('td')
            serial = tmp[0].text.strip()
            stunum = tmp[1].text.strip()
            stuDepartment = tmp[3].text.strip()
            tmp2     = tmp[4].text.strip().split("-")
            stuGrade = tmp2[0]
            stuClass = "*"
            if len(tmp2)>1:
                stuClass = tmp2[1]
            stuGender   = tmp[5].text.strip()
            stuRequired = tmp[6].text.strip()
            stuPriority = tmp[7].text.strip()
            stuStatus   = tmp[8].text.strip()
            
            stu_isDoc = "博士" in stuDepartment
            stu_isMas = "碩士" in stuDepartment
            stu_isRequired = "必修" in stuRequired
            stu_isPreselected = "初選" in stuStatus
            if stu_isPreselected:
                crs_preselecStu += 1
            
            if stuGender == "男":
                crs_stuGender['male'] += 1
            else:
                crs_stuGender['Female'] += 1
            
            if stu_isDoc:
                if stuGrade not in crs_stuGrade['doctor']:
                    crs_stuGrade['doctor'][stuGrade] = 0
                crs_stuGrade['doctor'][stuGrade] += 1
            if stu_isMas:
                if stuGrade not in crs_stuGrade['master']:
                    crs_stuGrade['master'][stuGrade] = 0
                crs_stuGrade['master'][stuGrade] += 1
            if not stu_isDoc and not stu_isMas:
                if stuGrade not in crs_stuGrade['bachelor']:
                    crs_stuGrade['bachelor'][stuGrade] = 0
                crs_stuGrade['bachelor'][stuGrade] += 1
            crs_stus.append({
                'serial'    :serial,
                'stunum'    :stunum,
                'department':stuDepartment,
                'grade'     :stuGrade,
                'class'     :stuClass,
                'priority'  :stuPriority,
                'isRequired':stu_isRequired,
                'isPreselected':stu_isPreselected})
    return {
        'department'    :crs_dept,
        'system'        :crs_system,
        'language'      :crs_lang,
        'card'          :crs_card,
        'assigned'      :crs_assigned,
        'selected'      :crs_selected,
        'remark'        :crs_remark,
        'goal'          :crs_goal,
        'outline'       :crs_outline,
        'textbook'      :crs_textbook,
        'selfCompiledRate':crs_selfCompiledRate,
        'instructMethod'  :crs_instructMethod,
        'gradMethod'      :crs_gradMethod,
        'officeHour'      :crs_officeHour,
        'teachWeeks'      :crs_teachWeeks,
        'flexDiscription' :crs_flexDiscription,
        'domain'          :crs_domain,
        'map'             :csr_map,
        'assignCriteria'  :crs_assignCriteria,
        'preselecStu'     :crs_preselecStu,
        'stuGender'       :crs_stuGender,
        'stuGrade'        :crs_stuGrade,
        'stus'            :crs_stus,
    }
    
def parse_course_detail_en(response):
    html = bs(response.text, 'html.parser')
    tables = html.find_all('table',class_='classBase')
    rows = tables[0].find_all('tr')
    crs_dept   = rows[4].find_all('td')[1].text.strip()
    crs_system = rows[5].find_all('td')[1].text.strip()
    crs_lang   = rows[10].find_all('td')[1].text.strip()
    crs_card   = rows[11].find_all('td')[1].text.strip()
    crs_assigned = int(rows[13].find_all('td')[1].text.strip())
    crs_selected = int(rows[14].find_all('td')[1].text.strip())

    crs_remark   = "\n".join(list(rows[15].find_all('td')[1].stripped_strings))
    crs_remark = re.sub(r'[\r\t]','',crs_remark)
    crs_goal     = "\n".join(list(rows[16].find_all('td')[1].stripped_strings))
    crs_goal = re.sub(r'[\r\t]','',crs_goal)
    crs_outline  = "\n".join(list(rows[17].find_all('td')[1].stripped_strings))
    crs_outline = re.sub(r'[\r\t]','',crs_outline)
    crs_textbook = "\n".join(list(rows[18].find_all('td')[1].stripped_strings))
    crs_textbook = re.sub(r'[\r\t]','',crs_textbook)

    crs_selfCompiledRate = rows[19].find_all('td')[1].text.strip()
    crs_instructMethod   = rows[20].find_all('td')[1].text.strip()
    crs_instructMethod = re.sub(r'[\r\t]','',crs_instructMethod)
    crs_instructMethod = crs_instructMethod.split("\n")

    crs_gradMethod       = "\n".join(list(rows[21].find_all('td')[1].stripped_strings))
    crs_gradMethod = re.sub(r'[\r\t]','',crs_gradMethod)
    crs_officeHour       = "\n".join(list(rows[22].find_all('td')[1].stripped_strings))
    crs_officeHour = re.sub(r'[\r\t]','',crs_officeHour)

    crs_teachWeeks       = rows[23].find_all('td')[1].text.strip()
    
    crs_flexDiscription  = "\n".join(list(rows[24].find_all('td')[1].stripped_strings))
    crs_flexDiscription = re.sub(r'[\r\t]','',crs_flexDiscription)

    crs_domain           = "\n".join(list(rows[25].find_all('td')[1].stripped_strings))
    crs_domain           = re.sub(r'[\r\t]','',crs_domain)

    temp = html.find_all('table',class_='courseMap')[0].find_all('tr')
    csr_map = []
    if len(temp) > 1:
        for tmp in temp[2:]:
            tmp = tmp.find_all('td') 
            csr_map.append({
                'competencies' :tmp[0].text.strip(),
                'rating'       :re.sub(r'\s+','',tmp[1].text.strip()),
                'assesments'   :[i.strip() for i in tmp[2].text.strip().split("，")],
            })
    temp = html.find_all('table',id='AutoNumber1')
    crs_assignCriteria = []
    if len(temp) != 0:
        temp = temp[0].find_all('tr')
        for tmp in temp[1:]:
            tmp = tmp.find_all('td')
            crs_assignCriteria.append(tmp[1].text.strip())
    
    temp = html.find_all('table',id='std')
    crs_preselecStu = 0
    crs_stuGender = {'male':0,'Female':0}
    crs_stuGrade  = {'doctor':{},'master':{},'bachelor':{}}
    crs_stus = []
    if len(temp) != 0:
        temp = temp[0].find_all('tr')
        for tmp in temp[1:]:
            tmp = tmp.find_all('td')
            serial = tmp[0].text.strip()
            stunum = tmp[1].text.strip()
            stuDepartment = tmp[3].text.strip()
            tmp2     = tmp[4].text.strip().split("-")
            stuGrade = tmp2[0]
            stuClass = "*"
            if len(tmp2)>1:
                stuClass = tmp2[1]
            stuGender   = tmp[5].text.strip()
            stuRequired = tmp[6].text.strip()
            stuPriority = tmp[7].text.strip()
            stuStatus   = tmp[8].text.strip()
            
            stu_isDoc = "PhD" in stuDepartment
            stu_isMas = "MsC" in stuDepartment
            stu_isRequired = "Required" in stuRequired
            stu_isPreselected = "preliminary" in stuStatus
            if stu_isPreselected:
                crs_preselecStu += 1
            
            if stuGender == "Male":
                crs_stuGender['male'] += 1
            else:
                crs_stuGender['Female'] += 1
            
            if stu_isDoc:
                if stuGrade not in crs_stuGrade['doctor']:
                    crs_stuGrade['doctor'][stuGrade] = 0
                crs_stuGrade['doctor'][stuGrade] += 1
            if stu_isMas:
                if stuGrade not in crs_stuGrade['master']:
                    crs_stuGrade['master'][stuGrade] = 0
                crs_stuGrade['master'][stuGrade] += 1
            if not stu_isDoc and not stu_isMas:
                if stuGrade not in crs_stuGrade['bachelor']:
                    crs_stuGrade['bachelor'][stuGrade] = 0
                crs_stuGrade['bachelor'][stuGrade] += 1
            crs_stus.append({
                'serial'    :serial,
                'stunum'    :stunum,
                'department':stuDepartment,
                'grade'     :stuGrade,
                'class'     :stuClass,
                'priority'  :stuPriority,
                'isRequired':stu_isRequired,
                'isPreselected':stu_isPreselected})
    return {
        'department'    :crs_dept,
        'system'        :crs_system,
        'language'      :crs_lang,
        'card'          :crs_card,
        'assigned'      :crs_assigned,
        'selected'      :crs_selected,
        'remark'        :crs_remark,
        'goal'          :crs_goal,
        'outline'       :crs_outline,
        'textbook'      :crs_textbook,
        'selfCompiledRate':crs_selfCompiledRate,
        'instructMethod'  :crs_instructMethod,
        'gradMethod'      :crs_gradMethod,
        'officeHour'      :crs_officeHour,
        'teachWeeks'      :crs_teachWeeks,
        'flexDiscription' :crs_flexDiscription,
        'domain'          :crs_domain,
        'map'             :csr_map,
        'assignCriteria'  :crs_assignCriteria,
        'preselecStu'     :crs_preselecStu,
        'stuGender'       :crs_stuGender,
        'stuGrade'        :crs_stuGrade,
        'stus'            :crs_stus,
    }