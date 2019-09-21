#Python3
import math, requests, time, mysql.connector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import yaml

class Scraper:

    def __init__(self):
        self.browser = webdriver.Firefox()

    #term: Fall 2019
    def handle_initial_page(self, class_name, class_num):
        print('here1')
        all_classes = self.browser.find_element_by_xpath('/html/body/div/form/div/div[2]/div[4]/div/select/option[2]')
        print('here2')
        print(all_classes)
        all_classes.click()
        print('here3')

        # path = '/html/body/div/form/div/div[2]/div[5]/div/div/select//option[@value="%s"]' % class_name
        path = '/html/body/div/form/div/div[2]/div[5]/div/div/select//option[@value="{}"]'.format(class_name)
        course_name = self.browser.find_element_by_xpath(path)
        course_name.click()

        course_number = self.browser.find_element_by_xpath('//*[@id="catalog_nbr"]')
        course_number.send_keys(class_num)

        search = self.browser.find_element_by_xpath('/html/body/div/form/div/div[2]/div[15]/div/input')
        time.sleep(2)
        search.click()

    def handle_class(self):
        #get all info needed from page
        subject = self.browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/h2').text
        class_number = self.browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div[2]/div/div[1]/dl/dd[3]').text
        status = self.browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div[2]/div/div[2]/dl/dd[1]').text
        available_seats = self.browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div[2]/div/div[2]/dl/dd[2]').text
        wait_list_total = self.browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div[2]/div/div[2]/dl/dd[6]').text
        return [class_number, status, available_seats, wait_list_total]

    def handle_page(self):
        time.sleep(2)       #be kind to server
        click_class = self.browser.find_element_by_css_selector('[id*="class_id_"]')
        click_class.click()
        return self.handle_class()

    def find_info(self, name_and_num):
        self.browser.get('https://pisa.ucsc.edu/class_search/index.php')
        full_name = name_and_num[:name_and_num.find(' - ')].split()
        class_name = full_name[0]
        num = full_name[1]
        self.handle_initial_page(class_name, num)
        return self.handle_page()

    def close_browser(self):
        self.browser.quit()
