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
    url = "https://www.levels.fyi/comp.html?track=Software%20Engineer&region=613&timerangeradio=Past%20Year"
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
                try:
                    csvwriter.writerows(get_table_data([row.text for row in table_data[1::]]))
                except Exception as e:
                    print(f'Error writing rows: {e}')
                turn_page(browser_session)
                time.sleep(random.uniform(6, 8))
    except requests.exceptions.RequestException as e:
        print(e)


def get_table(browser, url):
    browser.get(url)
    remove_region = browser.find_element_by_xpath('/html/body/div[2]/div/div[4]/div[1]/div[3]/div[2]/span[1]/i')
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
    next_page = browser.find_element_by_xpath(
        "/html/body/div[2]/div/div[4]/div[4]/div/div[1]/div[1]/div[3]/div[2]/ul/li[9]/a")
    next_page.click()


def get_table_data(row_texts: list[str]) -> list[[str]]:
    def strip(data):
        return data.strip()

    column_mapping = {
        0: strip,  # Company
        1: lambda data: [x.strip() for x in data.split('|')],  # Location, Date
        2: strip,  # Level
        3: strip,  # Tag
        4: lambda data: [x.strip() for x in data.split('/')],  # YAC & YOE
        5: strip,  # Total
        6: lambda data: [x.strip() for x in data.split('|')]
    }

    rows = []
    for text in row_texts:
        column_list = re.split("[\n]", text)
        try:
            # Handle salary bump
            if "+$" in column_list[5]:
                print("Removing salary bump")
                column_list.pop(5)

            row = []
            for i, column in enumerate(column_list):
                mapped = column_mapping[i](column)
                if type(mapped) is list:
                    row.extend(mapped)
                else:
                    row.append(mapped)
            if len(row) == 11:
                rows.append(row)
            else:
                print(f'Incorrect data length for row {column_list}')
        except Exception as e:
            print(f'Error parsing data: {column_list}, e: {e}')
    return rows


def get_table_headers(row: str):
    headers_text_list = re.split("[\n|]", row)

    def header_generator(headers):
        for header in headers:
            header = header.strip().lower()
            if header == "level name":
                yield "level"
            elif header == "at company / total":
                yield from (exp for exp in ["YAC", "YOE"])
            elif header == "stock (/yr)":
                yield "stock"
            elif header == "total compensation":
                yield "total"
            elif header != "years of experience":
                yield header

    res = list(header_generator(headers_text_list))
    assert (len(res) == 11), f'Not enough headers generated {res}'
    return res


if __name__ == '__main__':
    scrape()
