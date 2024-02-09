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
    print(f'Target department: {department_data["name"]["en"]}')
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
    
    
def fetch_course_detail(course_data):
    course_url = f'https://cis.ncu.edu.tw/Course/main/support/courseDetail.html?crs={course_data["serial"]}'
    print('[Work] Fetching course detail ......')
    print(f'Target course: {course_data["name"]["en"]}')
    reqter = Requester()
    response = reqter.getter(course_url)
    
    en_result = None
    ch_result = None
    
    if reqter.is_english():
        reqter.toggle_language()
        response = reqter.getter(course_url)
    
    print('Parsing Chinese course detail data ......')
    ch_result = parse_course_detail_ch(response)
    
    reqter.toggle_language()
    response = reqter.getter(course_url)
    
    print('Parsing English course detail data ......')
    en_result = parse_course_detail_en(response)
    
    validated = val_course_detail(en_result, ch_result)
    print('[Done] Course detail fetched ......')
    
    return {
        'serial'           :course_data['serial'           ],  
        'department_serial':course_data['department_serial'], 
        'code'             :course_data['code'          ],
        'class'            :course_data['class'         ], 
        'name'             :course_data['name'          ], 
        'notice'           :course_data['notice'        ], 
        'instructor'       :course_data['instructor'    ], 
        'credits'          :course_data['credits'       ], 
        'time_loc'         :course_data['time_loc'      ], 
        'isRequired'       :course_data['isRequired'    ], 
        'isFullSem'        :course_data['isFullSem'     ], 
        'MaxStu'           :course_data['MaxStu'        ], 
        'department'       :{'ch':ch_result['department'],
                             'en':en_result['department']},
        'system'           :{'ch':ch_result['system'  ],
                             'en':en_result['system'  ]},
        'language'         :{'ch':ch_result['language'],
                             'en':en_result['language']},
        'card'             :{'ch':ch_result['card'    ],
                             'en':en_result['card'    ]},
        'assigned'         :ch_result['assigned'        ],
        'selected'         :ch_result['selected'        ],
        'remark'           :{'ch':ch_result['remark'          ],
                             'en':en_result['remark'          ]},
        'goal'             :{'ch':ch_result['goal'            ],
                             'en':en_result['goal'            ]},
        'outline'          :{'ch':ch_result['outline'         ],
                             'en':en_result['outline'         ]},
        'textbook'         :{'ch':ch_result['textbook'        ],
                             'en':en_result['textbook'        ]},
        'selfCompiledRate' :{'ch':ch_result['selfCompiledRate'],
                             'en':en_result['selfCompiledRate']},
        'instructMethod'   :{'ch':ch_result['instructMethod'  ],
                             'en':en_result['instructMethod'  ]},
        'gradMethod'       :{'ch':ch_result['gradMethod'      ],
                             'en':en_result['gradMethod'      ]},
        'officeHour'       :{'ch':ch_result['officeHour'      ],
                             'en':en_result['officeHour'      ]},
        'teachWeeks'       :{'ch':ch_result['teachWeeks'      ],
                             'en':en_result['teachWeeks'      ]},
        'flexDiscription'  :{'ch':ch_result['flexDiscription' ],
                             'en':en_result['flexDiscription' ]},
        'domain'           :{'ch':ch_result['domain'          ],
                             'en':en_result['domain'          ]},
        'map'              :{'ch':ch_result['map'             ],
                             'en':en_result['map'             ]},
        'assignCriteria'   :{'ch':ch_result['assignCriteria'  ],
                             'en':en_result['assignCriteria'  ]},
        'preselecStu'      :ch_result['preselecStu'     ],
        'stuGender'        :ch_result['stuGender'       ],
        'stuGrade'         :ch_result['stuGrade'        ],
        'stus'             :ch_result['stus'            ],
    }

def fetch_semester():
    print('[Work] Fetching current semester ......')
    reqter = Requester()
    semester = reqter.current_semester()
    print(f'[Done] Current semester: {semester}')
    return semester
