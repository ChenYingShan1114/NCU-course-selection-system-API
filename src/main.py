from crawler import craw
import datetime
import os 
import json 

current_semester = craw.fetch_semester()
output_path = f"../api/{current_semester}"

initial_fetch = False

if not os.path.exists(output_path):
    initial_fetch = True
    os.makedirs(output_path)

colleges,departments = craw.fetch_departments()
json.dump(colleges,    open(f"{output_path}/colleges.json",    "w"),ensure_ascii=False)
json.dump(departments, open(f"{output_path}/departments.json", "w"),ensure_ascii=False)
all_courses = []

for index in range(len(departments)):
    print(f"On fetching department's courses, current->({index+1}/{len(departments)})")
    dep  = departments[index]
    courses = craw.fetch_courses(dep)
    all_courses += courses
json.dump(all_courses, open(f"{output_path}/all_course.json", "w"),ensure_ascii=False)

failed = []
fetched = set()
for index in range(len(all_courses)):
    course = all_courses[index]
    print(f"On fetching course detail, current->({index+1}/{len(all_courses)})")
    initial_fetch = False
    if course['serial'] in fetched:
        print(f"[Warning] Course serial:{course['serial']} has been fetched")
        continue
    try:
        course_detail = craw.fetch_course_detail(course)
        fetched.add(course['serial'])
    except Exception as e:
        print(e)
        print(f"[Fetal Error] Failed to fetch course detail for serial:{course['serial']}")
        course['error_msg'] = str(e)
        failed.append(course)
        continue
    
    if not os.path.exists(f"{output_path}/{course['serial']}"):
        print(f"[Initial fetch] Creating directory for course serial:{course['serial']}")
        os.makedirs(f"{output_path}/{course['serial']}")
        os.makedirs(f"{output_path}/{course['serial']}/history")
        initial_fetch = True
        statistics = {'timestamp':[datetime.datetime.now().timestamp()], 
                'data'     :{'selected':[course_detail['selected']],
                             'assigned':[course_detail['assigned']],
                             'preselecStu':[course_detail['preselecStu']],
                             'stuGender':[course_detail['stuGender']],}
        }
        json.dump(statistics, open(f"{output_path}/{course['serial']}/history/statistics.json", "w"),ensure_ascii=False)
    else:
        print(f'[Updating]course serial:{course["serial"]} directory already exists, updating statistics...')
        last_statistics = json.load(open(f"{output_path}/{course['serial']}/history/statistics.json"))
        last_statistics['timestamp'].append(datetime.datetime.now().timestamp())
        last_statistics['data']['selected'].append(course_detail['selected'])
        last_statistics['data']['assigned'].append(course_detail['assigned'])
        last_statistics['data']['preselecStu'].append(course_detail['preselecStu'])
        last_statistics['data']['stuGender'].append(course_detail['stuGender'])
        json.dump(last_statistics, open(f"{output_path}/{course['serial']}/history/statistics.json", "w"),ensure_ascii=False)
    
    json.dump(course_detail, open(f"{output_path}/{course['serial']}/detial.json", "w"),ensure_ascii=False)
    
    
    # stu_list history name (current date)
    his_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    json.dump(course_detail['stus'], open(f"{output_path}/{course['serial']}/history/{his_name}.json", "w"),ensure_ascii=False)

print("=========================================")
print("=Generating semester fetch status report=")
est_total_course = 0
for dep in departments:
    est_total_course += dep['course_cnt']
status = {'update_time':datetime.datetime.now().strftime('%Y-%m-%d-%H-%M'),
          'total_colleges'   :len(colleges),
          'total_departments':len(departments), 
          'estimated_total_courses':est_total_course,
          'total_courses'    :len(all_courses),
          'detail_actual_fetched'   :len(fetched),
          'duplicate'        :len(all_courses) - len(fetched),
          'failed'           :len(failed)}

json.dump(status, open(f"{output_path}/status.json", "w"),ensure_ascii=False)
json.dump(failed, open(f"{output_path}/failed.json", "w"),ensure_ascii=False)
print("================Work Done===============")
print("================ reports ===============")
print(f"Total colleges          :{len(colleges)}")
print(f"Total departments       :{len(departments)}")
print(f"Estimated total courses :{est_total_course}")
print(f"Total courses           :{len(all_courses)}")
print(f"Detail actual fetched   :{len(fetched)}")
print(f"Duplicate               :{len(all_courses) - len(fetched)}")
print(f"Failed                  :{len(failed)}")
print("========================================")
# output api status
api_status = json.load(open(f"../api/status.json"))
api_status["updatetime"] = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
api_status["current_semester"] = current_semester
api_status["all_semesters"]    = list(set(api_status["all_semesters"] + [current_semester]))
json.dump(api_status, open(f"../api/status.json", "w"),ensure_ascii=False)