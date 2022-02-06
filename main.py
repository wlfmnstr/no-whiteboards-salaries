import random
import re
import time
import csv
from typing import List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from requests_html import HTMLSession
# from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # Use a breakpoint in the code line below to debug your script.
    url = "https://www.levels.fyi/comp.html?track=Software%20Engineer&yoestart=2&yoeend=5&yoeradio=Mid%20Level" \
          "&timerangeradio=Past%20Year "
    try:
        browser = webdriver.Chrome(ChromeDriverManager().install())
        table, browser_session = get_table(browser, url)
        table_data: list[WebElement] = table.find_elements_by_tag_name('tr')
        table_headers = get_table_headers(table_data[0].text)
        page_count = int(browser.find_element_by_xpath(
            '/html/body/div[2]/div/div[4]/div[4]/div/div[1]/div[1]/div[3]/div[2]/ul/li[8]/a').text)
        file_name = "./engineering-salaries.csv"
        with open(file_name, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(table_headers)
            for page in range(page_count):
                table_data = table.find_elements_by_tag_name('tr')
                csvwriter.writerows(get_table_data([row.text for row in table_data[1::]]))
                turn_page(browser_session)
                time.sleep(random.uniform(1.5, 3))
    except requests.exceptions.RequestException as e:
        print(e)


def get_table(browser, url):
    browser.get(url)
    remove_region = browser.find_element_by_xpath('/html/body/div[2]/div/div[4]/div[1]/div[3]/div[2]/span[3]/i')
    remove_region.click()
    time.sleep(1)
    click_to_sort = browser.find_element_by_xpath('//*[@id="compTable"]/thead/tr/th[5]')
    time.sleep(1)
    click_to_sort.click()
    time.sleep(1)
    click_to_sort.click()
    time.sleep(1)
    drop_down = browser.find_element_by_xpath(
        '/html/body/div[2]/div/div[4]/div[4]/div/div[1]/div[1]/div[3]/div[1]/span[2]/span')
    drop_down.click()
    drop_down.click()
    drop_down.click()
    select_100 = browser.find_element_by_xpath(
        '/html/body/div[2]/div/div[4]/div[4]/div/div[1]/div[1]/div[3]/div[1]/span[2]/span/ul/li[4]')
    select_100.click()
    time.sleep(3)
    comp_table = browser.find_element_by_id('compTable')
    return comp_table, browser


def turn_page(browser):
    next_page = browser.find_element_by_css_selector("li.page-item.page-next > a")
    next_page.click()


def get_table_data(row_texts: list[str]) -> list[[str]]:
    def row_generator(data):
        columns = re.split("[\n]", data)
        """ NAME """
        yield columns[0]
        """ LOCATION & DATE """
        yield from (column.strip() for column in columns[1].split('|'))
        """ Level & Tag """
        yield from (columns[2], columns[3])
        """ YAC & YOE """
        yield from (column.strip() for column in columns[4].split('/'))
        """ Total """
        yield columns[5]
        """ Base, Stock, Bonus """
        yield from (column.strip() for column in columns[6].split('|'))

    return [list(row_generator(row_data)) for row_data in row_texts]


def get_table_headers(row: str):
    headers_text_list = re.split("[\n|]", row)

    def header_generator(headers):
        for header in headers:
            header = header.strip().lower()
            if header == "level name":
                yield "level"
            elif header == "at company / total":
                yield from ("YAC", "YOE")
            elif header == "stock (/yr)":
                yield "stock"
            elif header != "years of experience":
                yield header

    res = list(header_generator(headers_text_list))
    assert (len(res) == 11), f'Not enough headers generated {res}'
    return res


if __name__ == '__main__':
    scrape()
