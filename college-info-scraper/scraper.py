import os
import re
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

def init_csv():
    # Make the csv if it doesn't exist
    if not os.path.exists('college_info.csv'):
        os.system('touch college_info.csv')
        with open('college_info.csv',mode='w') as f:
            f.write('Rank,Name,Engineering Rank,In-State,Out-of-State,Acceptance Rate,'\
                    'Standardized Tests,Application Deadline,Accepts Common App')
            f.write('\n')
        
def scrape(url):
    # Set chromedriver options to run headless (no external browser window) and set user agent to trick website
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    chrome_options.add_argument('user-agent={userAgent}')
    
    # Pass the url to the driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # Parse the page source as lxml
    main_soup = BeautifulSoup(driver.page_source, 'lxml')
    
    # Find rank of school
    rank_header = main_soup.find('span', attrs={'class': 'ProfileHeading__RankingSpan-esdqt6-3 lcCek'})
    try:
        ranking = rank_header.find_all('span', attrs={'class': None})[0].contents[0]
    except:
        ranking = ''
    # Find name of school
    name_soup = main_soup.find('h1', attrs={'class': 
        'Heading__HeadingStyled-sc-1w5xk2o-0 fGFsEE Heading-sc-1w5xk2o-1 Wakanda__Title-rzha8s-10 cBNzjc'})
    name = name_soup.contents[0] + name_soup.find('span', attrs={'class': 'HeadingWithIcon__NoWrap-sc-1kfmde2-1 kNLxOL'}).contents[0]
    # Find in-state + out-of-state
    cost_table = main_soup.find_all('div', attrs={'class': 'Box-w0dun1-0 DataRow__Row-sc-1udybh3-0 hPMEGt', 'spacing': "4"})
    in_state = cost_table[0].find_all('a', attrs={'class': 'Anchor-byh49a-0 elcbWB'})[0].contents[0]
    in_state = re.sub('\\*','',in_state)
    out_state = cost_table[1].find_all('a', attrs={'class': 'Anchor-byh49a-0 elcbWB'})[0].contents[0]
    out_state = re.sub('\\*','',out_state)
    
    # Find engineering rank
    ranking_spec = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[4]/div/nav[1]/div/div/div[2]/div/div/ul/li[2]/a')
    ranking_spec.send_keys(Keys.RETURN)
    # soup for rankings page
    rank_soup = BeautifulSoup(driver.page_source, 'lxml')
    x = rank_soup.find_all('a', attrs={'class': 'Anchor-byh49a-0 hjkTf', 'href': 'https://www.usnews.com/best-colleges/rankings/engineering-doctorate'})[0]
    engineering_rank = x.find_all('strong', attrs={'style': 'vertical-align:top'})[0].text

    # Navigate to admissions page and get rest of parameters
    admissions_spec = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[4]/div/nav[1]/div/div/div[2]/div/div/ul/li[4]/a')
    admissions_spec.send_keys(Keys.RETURN)
    # soup for admissions
    admission_soup = BeautifulSoup(driver.page_source, 'lxml')
    # acceptance rate + deadline
    stats = admission_soup.find_all('dd', attrs={'class': 
        'QuickStat__Description-sc-1m0tve6-1 HUVrp QuickStat-sc-1m0tve6-3 mwRIi QuickStat-sc-1m0tve6-4 csJJeU'})
    deadline = stats[0].contents[0]
    acceptance_rate = stats[2].contents[0]
    # standardized tests
    f = admission_soup.find_all('div', attrs={'class': 'section-box'})[2]
    tests = f.find_all('p', attrs={'class': 'Paragraph-sc-1iyax29-0 gynMKH'})[1].contents[0]
    # common app status
    g = admission_soup.find_all('div', attrs={'class': 'section-box'})[1]
    common_app = g.find_all('p', attrs={'class': 'Paragraph-sc-1iyax29-0 gynMKH'})[3].contents[0]
    common_app = False if common_app == 'No' else True
    # write to csv
    with open('college_info.csv', 'a+') as csv:
        lines = csv.read().splitlines()
        in_state = re.sub(',','',in_state).strip()
        out_state = re.sub(',','',out_state).strip()
        formString = f'{ranking},{name},{engineering_rank},{in_state},{out_state},{acceptance_rate},{tests},{deadline},{common_app}'
        if formString not in lines:
            csv.write(formString)
            csv.write('\n')
            print(f'Added {name} to CSV')
                
if __name__ == "__main__":
    init_csv()
    with open('urls.txt', 'r') as file:
        for url in file.readlines():
            scrape(url)
