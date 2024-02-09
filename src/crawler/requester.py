import requests
from bs4 import BeautifulSoup as bs
# Header for the request

class Requester:
    main_session = requests.session()
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/58.0.3029.110 Safari/537.3'
    } 
    main_url = 'https://cis.ncu.edu.tw/Course/main/news/announce'

    def __init__(self):
        # Initial request to get the cookies
        self.main_session.get(self.main_url, headers=self.headers)
    
    # Function to make a request to the given url
    # Returns the response if the request is successful
    def getter(self, url):
        response = self.main_session.get(url, headers=self.headers)
        response.raise_for_status()
        return response

    
    def toggle_language(self):
        self.getter('https://cis.ncu.edu.tw/Course/main/lang')
    
    def is_english(self):
        response = self.getter(self.main_url)
        html = bs(response.text, 'html.parser')
        lang_tag = html.find_all('a', class_='intro lang')[0].text
        return lang_tag!='English'
    
    def current_semester (self):
        response = self.getter(self.main_url)
        html = bs(response.text, 'html.parser')
        sem = html.find_all('a', class_='intro_banner')[1].text.split("|")[0].strip()
        return sem