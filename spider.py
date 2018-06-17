import json

from selenium import webdriver 
from scrapy.http import HtmlResponse
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

results = []


def parse(response):

    #for comment in response.css('div.comment-list-item'):
    for comment in response.css('div.comment-item-wrapper'):
       result = {
        
               'username' : comment.xpath('.//a[@class = "username"]/text()').extract_first().strip(),

               'content' : comment.xpath('.//div[contains(@class , "comment-item-content")]/p/text()').extract_first()

       }
       results.append(result)  
       
def has_next_page(response):
    #s = response.xpath('//li[@class="disabled next-page"]').extract_first()
    s = response.css('li.disabled.next-page').extract_first()
    if s == None: 
        return 1
    return 0
     
def goto_next_page(driver): 
    '''
    ac = driver.find_element_by_css_selector('div.comment-box li.next-page a')
    ActionChains(driver).move_to_element(ac).perform()
    ps1 = driver.find_element_by_xpath('//li[contains(@class,"next-page"]')
    '''
    ps1 = driver.find_element_by_css_selector('div.comment-box li.next-page')
    ps1.click()


  #  ActionChians(driver).move_to_element(ps1).perform() 

  # ActionChians(driver).move_to_element(ps1).click(ps1).perform()

def wait_page_return(driver,page):

    WebDriverWait(driver,10).until(
        EC.text_to_be_present_in_element(
            (By.XPATH,'//ul[@class="pagination"]/li[@class="active"]'),
            str(page)
        )
    )   
         
def spider():
  
    driver = webdriver.PhantomJS()

    url = 'https:www.shiyanlou.com/courses/427'

    driver.get(url)

    page = 1

    while True:

        wait_page_return(driver,page)

        html = driver.page_source

        response = HtmlResponse(url=url,body=html.encode('utf8'))

        parse(response)
        print('--------------', page)
        if not has_next_page(response):
        #if response.css('div.comment-box li.disabled.next-page'):
            driver.quit()
            break
        page += 1

        goto_next_page(driver)

    with open('/home/shiyanlou/comments.json','w') as f:

        f.write(json.dumps(results))

if __name__ == '__main__':

    spider()

    
