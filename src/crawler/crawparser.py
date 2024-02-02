from bs4 import BeautifulSoup as bs
import re

# Parse current page and return current language setting 
def is_english(response):
    html = bs(response.text, 'html.parser')
    lang_tag = html.find_all('a', class_='intro lang')[0].text
    return lang_tag!='English'

# Function that parses the department page and returns a dictionary,
# containing the department name, url to the department contained course page 
# and the total number of courses in the department
def parse_department(response):
    html = bs(response.text, 'html.parser')
    items = html.find_all('li')
    results = []
    for item in items:
        dep_url = 'https://cis.ncu.edu.tw' + item.a.get("href")
        dep_info_text = item.a.text.strip()
        matches = re.findall('\((.*?)\)', dep_info_text)
        if matches is not None:
            # Potential bug: if cannot convert to int (Needs handle)
            dep_courses = int(matches[-1])
            dep_name = re.sub(f'\({dep_courses}\)', '', dep_info_text)
        else :
            print('Failed to parse department info when : ' + dep_info_text)
            dep_courses = 'N/A'
            dep_name = dep_info_text
        results.append({
            'name'   : dep_name,
            'url'    : dep_url,
            'courses': dep_courses,
        })
    return results


