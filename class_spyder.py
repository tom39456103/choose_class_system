#!/usr/bin/env python
# coding: utf-8

# In[50]:


import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import urllib



# college_y = '112#2'#學年(年#學期)
# dpt = '理學院'#院(全名)
# unt = '數學系'#系(全名)

def class_spyder(college_y = '112#2', dpt = '理學院', unt = '數學系', grade = 2):
    driver = webdriver.Chrome()
    url = 'https://shcourse.utaipei.edu.tw/utaipei/ag_pro/ag304.jsp?'
    #等待載入
    driver.get(url)
    time.sleep(1)
    try:
        find_frame = driver.find_element(By.NAME, '304_top')

        #driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])
        driver.switch_to.frame(find_frame)

        # 使用Select定位下拉式標籤
        selectyms = Select(driver.find_element(By.NAME, 'yms_yms'))
        # 選擇下拉式標籤中的選項
        selectyms.select_by_value(college_y)

        # 再等待一些時間，以確保網頁已經根據選擇刷新
        time.sleep(0.1)

        # 使用Select定位下拉式標籤
        selectdpt = Select(driver.find_element(By.NAME, 'dpt_id'))
        # 選擇下拉式標籤中的選項
        selectdpt.select_by_visible_text(dpt)

        # 再等待一些時間，以確保網頁已經根據選擇刷新
        time.sleep(0.1)


        # 使用Select定位下拉式標籤
        selectunt = Select(driver.find_element(By.NAME, 'unt_id'))
        # 選擇下拉式標籤中的選項
        selectunt.select_by_visible_text(unt)


        button = driver.find_element(By.ID, 'unit_serch')
        button.click()

        time.sleep(0.1)
        driver.switch_to.default_content()
    except:
        print('輸入有問題')
        driver.quit()
        return 0
    try:
        # 切換到NAME為 "304_bottom"
        frame_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, '304_bottom'))
        )
        driver.switch_to.frame(frame_element)
        grade = 2
        xpth = '/html/body/form/table/tbody/tr[2]/td[' + chr(grade + 48) + ']/div/u'

        # 找到包含 onclick 事件的 div 元素
        div_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpth))
        )

        # 使用 execute_script 方法執行 JavaScript 代碼點擊該元素
        driver.execute_script("arguments[0].click();", div_element)

        #確保頁面有足夠的時間處理事件
        WebDriverWait(driver, 10).until(
            EC.staleness_of(div_element)  # 等待元素消失，表示頁面已經完成相應的操作
        )


    except:
        print('請到網路好的地方使用\n')
        driver.quit()
        return 0

    # 取得網頁內容
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.find('table', {'align':'center'})
    columns = [td.text.replace('\n', '') for td in table.find('tr').find_all('td')]
    #print(columns)#條目                                                 範例輸出
    trs = table.find_all('tr')[1:]
    rows = list()
    for tr in trs:
        rows.append([td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td')])
    #時間字符處裡
    num8 = 0
    old_num8 = num8
    chforsc = True
    firstar = True
    for sys in rows[:]:
        str8 = sys[8]
        num8 = 0
        for ch in str8:
            oldnum8 = num8

            if ch == '一' :
                if firstar == False :num8*=100
                num8+=1
                firstar = False
            elif ch == '二' :
                if firstar == False :num8*=100
                num8+=2
                firstar = False
            elif ch == '三' :
                if firstar == False :num8*=100
                num8+=3
                firstar = False
            elif ch == '四' :
                if firstar == False :num8*=100
                num8+=4
                firstar = False
            elif ch == '五' :
                if firstar == False :num8*=100
                num8+=5
                firstar = False

            if ch == '(': chforsc = False
            if ch == ')': chforsc = True

            if '1' <= ch <= '9' and chforsc :
                num8 += int(ch)

            if(num8 != oldnum8):    
                num8*=10
        sys[11] = int(num8/10)
        #print(sys)                                                  範例輸出

    driver.quit()
    return rows
