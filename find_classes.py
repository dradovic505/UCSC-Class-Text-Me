#Python3
#source env/bin/activate
import math, requests, time, mysql.connector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import yaml

#I'm using firefox
browser = webdriver.Firefox()
browser.get('https://pisa.ucsc.edu/class_search/index.php')

########Functions#########

#term: Fall 2019
def handle_initial_page(class_name, class_num):
    all_classes = browser.find_element_by_xpath('/html/body/div/form/div/div[2]/div[4]/div/select/option[2]')
    all_classes.click()

    # path = '/html/body/div/form/div/div[2]/div[5]/div/div/select//option[@value="%s"]' % class_name
    path = '/html/body/div/form/div/div[2]/div[5]/div/div/select//option[@value="{}"]'.format(class_name)
    course_name = browser.find_element_by_xpath(path)
    course_name.click()

    course_number = browser.find_element_by_xpath('//*[@id="catalog_nbr"]')
    course_number.send_keys(class_num)

    search = browser.find_element_by_xpath('/html/body/div/form/div/div[2]/div[15]/div/input')
    time.sleep(2)
    search.click()

def handle_class():
    #get all info needed from page
    subject = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/h2').text
    class_number = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div[2]/div/div[1]/dl/dd[3]').text
    status = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div[2]/div/div[2]/dl/dd[1]').text
    available_seats = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div[2]/div/div[2]/dl/dd[2]').text
    wait_list_total = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div[2]/div/div[2]/dl/dd[6]').text

def handle_page():
    time.sleep(2)       #be kind to server
    click_class = browser.find_element_by_css_selector('[id*="class_id_"]')
    click_class.click()
    handle_class()

########End functions########

#one class for now
# full_name = thing from redis like 'ANTH 1 - 01'
full_name = 'ANTH 1 - 01'
name_and_num = full_name[:full_name.find(' - ')].split()
partial_name = name_and_num[0]
num = name_and_num[1]
handle_initial_page(partial_name, num)
handle_page()
browser.quit()
