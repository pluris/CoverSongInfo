from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import json
import os

DECADES_INFO = [
    '1900',
    '1910',
    '1920',
    '1930',
    '1940',
    '1950',
    '1960',
    '1970',
    '1980',
    '1990',
    '2000'
]
REDLIST_DECADES = [
    'https://www.youtube.com/playlist?list=PLqKKD5ka-57BbIfJlpmoNgBH4sIWuFGcE', # 1900
    'https://www.youtube.com/playlist?list=PLyOmKYxbnqjs3GK3rGParH1FzP-almCWs', # 1910
    'https://www.youtube.com/playlist?list=PLXRivw5Pd9qlM5efsL4c7js8teYFVy3Dk', # 1920
    'https://www.youtube.com/playlist?list=PLF0A3FC3B01A0DF8F', # 1930
    'https://www.youtube.com/playlist?list=PLRZlMhcYkA2Fhwg-NxJewUIgm01o9fzwB', # 1940
    'https://www.youtube.com/playlist?list=PLGBuKfnErZlBbRsqcuGy2lhb0xf931u-v', # 1950
    'https://www.youtube.com/playlist?list=PLGBuKfnErZlCkRRgt06em8nbXvcV5Sae7', # 1960
    'https://www.youtube.com/playlist?list=PLGBuKfnErZlCnsp1WWMqy-LHlvpCj_RuX', # 1970
    'https://www.youtube.com/playlist?list=PLGBuKfnErZlDYOaD2bOazzCYvy13ozt7C', # 1980
    'https://www.youtube.com/playlist?list=PLGBuKfnErZlAH3yaYBpIXra0HxFGEJKsB', # 1990
    'https://www.youtube.com/playlist?list=PL05E1623111A9A860' # 2000
]

def getDecadesData():
    delay = 3
    browser = Chrome('C:\chromedriver_win32\chromedriver.exe')
    result_list = []
    result_all_list = {}
    result_all_list['info'] = []
    for d_idx in range(len(REDLIST_DECADES)):
        start_url = REDLIST_DECADES[d_idx]
        browser.get(start_url)
        # browser.maximize_window()
        browser.implicitly_wait(delay)

        SCROLL_PAUSE_TIME = 0.5

        # 스크롤 제일 마지막 아래 대상 선택
        index = 0
        element_len = len(browser.find_elements_by_css_selector('ytd-playlist-video-renderer'))
        while True:
            index += 10
            if index >= element_len - 1:
                index =  element_len - 1
            element = browser.find_elements_by_css_selector('ytd-playlist-video-renderer')[index]
            # ELEMENT 가 화면에 보이도록 스크롤 조정 --> 아래 부분 추가로 확장됨
            browser.execute_script("arguments[0].scrollIntoView(true);", element)
            element_len = len(browser.find_elements_by_css_selector('ytd-playlist-video-renderer'))
            time.sleep(SCROLL_PAUSE_TIME)
            if index == element_len - 1:
                break

        page_src = browser.page_source
        p_html = BeautifulSoup(page_src, 'html.parser')
        parse_result = p_html.find("ytd-playlist-video-list-renderer")
        # print(parse_result)
        title_result = parse_result.find_all('span', {'id': 'video-title'})
        # Todo : Will be add playtime
        #playtime_result = parse_result.find_all('span', {'class': 'style-scope ytd-thumbnail-overlay-time-status-renderer'})
        playid_result = parse_result.find_all('a', {'class': 'yt-simple-endpoint style-scope ytd-playlist-video-renderer'})
        img_result = parse_result.find_all('img', {'class': 'style-scope yt-img-shadow'})
        data_set = {}
        song_info_list = []

        for idx in range(len(title_result)):
            if '삭제' in title_result[idx]['title']: continue
            else:
                playid = playid_result[idx]['href'].replace('/watch?v=','').split('&')[0]
                song_info_list.append({
                    'title': title_result[idx]['title'],
                    'thumbnail': img_result[idx]['src'],
                    'play_id': playid,
                })
        data_set['info'] = song_info_list
        result_list.append(data_set)
        result_all_list['info'].extend(song_info_list)
    return result_list, result_all_list


def makeDecadesjson(listdata):
    for d_idx in range(len(REDLIST_DECADES)):
        result_json = json.dumps(listdata[d_idx], indent=4, ensure_ascii=False)
        filename = f'../song_info/{DECADES_INFO[d_idx]}.json'
        if os.path.isfile(filename):
            os.remove(filename)
        with open(filename, 'w', encoding='UTF-8-sig') as json_file:
            json_file.write(result_json)


def makeAlljson(listdata):
    result_json = json.dumps(listdata, indent=4, ensure_ascii=False)
    filename = f'../song_info/all.json'
    if os.path.isfile(filename):
        os.remove(filename)
    with open(filename, 'w', encoding='UTF-8-sig') as json_file:
        json_file.write(result_json)


def getLoadJsonData():
    result_list = []
    for d_idx in range(1):
        filename = f'../song_info/{DECADES_INFO[d_idx]}.json'
        with open(filename, encoding='UTF-8-sig') as json_file:
            json_data = json.load(json_file)
            print(json_data['info'])
            result_list.append(json_data)
    return result_list


def getPopularDataList100(result_list):
    result_list = {}
    return result_list


if __name__ == "__main__":
    result_list, all_list = getDecadesData()
    makeDecadesjson(result_list)
    makeAlljson(all_list)
    # getLoadJsonData()
    #getPopularDataList100(result_list)