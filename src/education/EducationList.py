from src.education.Education import Education
from src.logic.FetcherAccount import FetcherAccount
from typing import List, Tuple
from bs4 import BeautifulSoup, ResultSet
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class EducationList:
    chrome_options:Options
    account:FetcherAccount
    soup:BeautifulSoup
    education_elements:ResultSet
    text:str
    def __init__(self, link:str, account:FetcherAccount):
        self.education_list:List[Education] = []
        self.link: str = f"{link}details/education/"
        self.account = account
    
    def parse(self):
        self.text = self.account.get_html(self.link)
        self.soup = BeautifulSoup(self.text, "html.parser")
        self.education_elements = self.soup.find_all('li', class_='pvs-list__paged-list-item')
        if self.education_elements is None:
            return
        for element in self.education_elements:
            major = self.get_degree(element)
            school = self.get_university_name(element)
            date_range = self.get_date_range(element)
            details_skills = self.get_skills_details(element)
            details = details_skills[0]
            skills =  details_skills[1]
            education = Education(major, school, date_range, details, skills)
            self.education_list.append(education)

    def get_university_name(self, element:ResultSet) -> str:
        university_div = element.find('div', class_='display-flex flex-wrap align-items-center full-height')
        university_name = "N/A"
        if university_div is None:
            return university_name
        university_element = university_div.find('span')
        if university_element is None:
            return university_name
        return university_element.getText(strip=True)
    
    def get_degree(self, element:ResultSet) -> str:
        degree_span = element.find('span', class_='t-14')
        degree = "N/A"
        if degree_span is None:
            return degree
        degree_span = degree_span.find('span', attrs={'aria-hidden': 'true'})
        return degree if degree_span is None else degree_span.getText(strip=True)

    def get_date_range(self, element:ResultSet) -> str:
        date_range_element = element.find('span', class_='t-14 t-normal t-black--light')
        date_range = "N/A"
        if date_range_element is None:
            return date_range
        date_range_element = date_range_element.find('span')
        if date_range_element is None:
            return date_range
        return date_range_element.getText(strip=True)

    def get_skills_details(self, element:ResultSet) -> Tuple[str, List[str]]:
        details = ""
        skill = ""
        skills:List[str] = []
        info = element.find('ul', class_='pvs-list')
        if info is None:
            return "N/A", skills
        info = info.find_all('span')
        if info is None:
            return "N/A", skills
        for i in info:
            if found_skills := i.find('span', class_='white-space-pre'):
                skill = i.get_text(strip=True)
            elif i.has_attr('class') and i['class'][0] == 'visually-hidden':
                text = i.get_text(strip=True)
                if details != text:
                    details = details + text + "\n"

        if skill != "":
            index = skill.find("Skills:")
            if index != -1:
                skill = skill[index+7:]
                skills = skill.split("\u00b7")
                skills = [i.strip() for i in skills]
        return details, skills
    
    def print(self):
        print(self.link)
        for education in self.education_list:
            print(education)




