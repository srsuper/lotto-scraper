import time

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


#last_url = 'https://www.dhlottery.co.kr/gameResult.do?method=byWin'
base_url = 'https://myplaybet.com'

def _scraper(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    return soup

def _parser(soup):
    # <meta id="desc" name="description" content="동행복권 931회 당첨번호 14,15,23,25,35,43+32. 1등 총 8명, 1인당 당첨금액 2,957,108,063원.">
    content = soup.find('div', {'id': 'result-table'})['content']

    # content: '동행복권 931회 당첨번호 14,15,23,25,35,43+32. 1등 총 8명, 1인당 당첨금액 2,957,108,063원.'
    sync = 'รอผล'
    if content.index(sync) != 0:
        raise Exception('No found start string.')

    s_idx = len(sync)
    e_idx = content.index('ไม่มีรอบ')

    #content = content[s_idx:e_idx]
    # content: '931회 당첨번호 14,15,23,25,35,43+32'
    #content = content.replace('회 당첨번호 ', ',')
    #content = content.replace('+', ',')

    #numbers = tuple(map(int, content.split(',')))

    #return numbers

def _last_number():
    soup = _scraper(last_url)
    nums = _parser(soup)

    return nums

def get_numbers(draw_no=0):
    last_nums = _last_number()

    if draw_no < 0 or draw_no > last_nums[0]:
        raise Exception('Invalid draw_no.')

    if draw_no == 0 or draw_no == last_nums[0]:
        return last_nums

    soup = _scraper(base_url + str(draw_no))
    nums = _parser(soup)

    return nums

def get_all_numbers():
    all_list = []
    last_nums = _last_number()

    for i in tqdm(range(1, last_nums[0])):
        soup = _scraper(base_url + str(i))
        nums = _parser(soup)

        all_list.append(nums)
        time.sleep(3)

    all_list.append(last_nums)

    return all_list


if __name__ == '__main__':
    nums = get_numbers()
    print(nums)
