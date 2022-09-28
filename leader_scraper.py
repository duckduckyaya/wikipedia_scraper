from functools import lru_cache
import requests
import re
import json
from bs4 import BeautifulSoup

root_url = 'https://country-leaders.herokuapp.com'
countries_url = "/countries"
leaders_url = "/leaders"
countries_url = "/countries"
cookie_url = '/cookie'




def get_first_paragraph(wiki_url, session):
    
    request = session.get(wiki_url).text
    new_soup = BeautifulSoup(request, 'html.parser') 
    paragraphs = new_soup.find_all('p')

    i = 0
    index = 0
    for para in paragraphs:
        if para.find('b') != None:
            index = i
        i+=1
    first_paragraph = paragraphs[index].text
    #print(first_paragraph)
    return first_paragraph



@lru_cache(maxsize=None,typed=False)
def get_leaders():
    cookies = requests.get(root_url + cookie_url)
    #check cookie_status
    cookie_status = cookie.status_code
    if cookie_status == 200:
        print("cookie is fine")
    else:
        response = requests.get(root_url+cookie_url")
        
    countries = requests.get(root_url+countries_url, cookies=cookie.cookies).json()
    leaders_per_country = {}
    #loop over the countries
    for i in range(len(countries)):
        country = countries[i]
        param = {
            "country" : country
            }
            
        #leaders requests
        leaders = requests.get(root_url+leaders_url, params=param, cookies=cookie.cookies).json()
        leaders_per_country[countries[i]] = leaders
        #print(type(leaders))
        
        for leader in leaders:
            wiki_url = leader['wikipedia_url']
            #print(leader)
            wiki_page = get_first_paragraph(wiki_url)
            leader['wiki_page'] = wiki_page
            return(leader)

def save(f):
    file = open(f, 'r')
    file.close