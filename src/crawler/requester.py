import requests

# Header for the request

class Requester:
    cookies = None
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/58.0.3029.110 Safari/537.3'
    } 
    
    def __init__(self):
        # Initial request to get the cookies
        url = 'https://cis.ncu.edu.tw/Course/main/news/announce'
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        self.update_cookies(response.cookies)
    
    # Function to make a request to the given url
    # Returns the response if the request is successful
    def getter(self, url):
        try:
            response = requests.get(url, headers=self.headers, cookies=self.cookies)
            response.raise_for_status()
            self.update_cookies(response.cookies)
            return response
        except requests.exceptions.HTTPError as http_err:
            print('==================================')
            print(f'HTTP error occurred: {http_err}')
            print('==================================')
        except Exception as err:
            print('==================================')
            print(f'An error occurred: {err}')
            print('==================================')
        return None

    def update_cookies(self, new_cookies):
        self.cookies = new_cookies
    
    def toggle_language(self):
        self.getter('https://cis.ncu.edu.tw/Course/main/lang')