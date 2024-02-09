def log_message(key, en_data, ch_data):
    print('[Fatel error] en & ch  data mismatched')
    print(f'==================[{key} mismatch]===================')
    print('En: ' + str(en_data))
    print('Ch: ' + str(ch_data))
    print('Job aborted due to Fatel error.')

def val_departmrnts(en_dat,ch_dat):
    validate_keys = ['url', 'course_cnt','facility_ser']
    # check length of the two lists
    if len(en_dat) != len(ch_dat):
        log_message('length', len(en_dat), len(ch_dat))
    for index in range(len(en_dat)):
        for key in validate_keys:
            if en_dat[index][key] != ch_dat[index][key]:
                log_message(key, en_dat, ch_dat)
                return False
    return True

def val_course_info(en_dat,ch_dat):
    
    validate_keys = ['serial'   ,
                     'code'     ,
                     'class'    , 
                     'credits'   ,
                     'required' ,
                     'isFulSem' ,
                     'max_stu'  , ]
    for key in validate_keys:
        if en_dat[key] != ch_dat[key]:
            log_message(key, en_dat, ch_dat)
            return False
    return True

def val_course_detail(en_dat,ch_dat):
    
    validate_keys = ['serial'   ,
                     'code'     ,
                     'class'    , 
                     'credits'   ,
                     'required' ,
                     'isFulSem' ,
                     'max_stu'  ,
                     'assigned'  ,
                     'selected'  ,
                     'prelim_sel',
                     'gender'    , ]
    for key in validate_keys:
        if en_dat[key] != ch_dat[key]:
            log_message(key, en_dat, ch_dat)
            return False
    return True