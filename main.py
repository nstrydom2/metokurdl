import lxml
import re
import wget
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from driver import Driver


def retrieve_video_links(driver):
    print('[*] Scraping links')

    metokur_url = 'https://www.bitchute.com/channel/x1VfONp6EI1a/'
    driver.open_url(metokur_url)
    scroll_to_bottom(driver.web_driver)
    soup = BeautifulSoup(driver.web_driver.page_source, 'html.parser')
    links = soup.findAll('a')

    mp4_links = []
    for link in links:
        try:
            if '/video' in link.attrs['href']:
                mp4_links.append(link.attrs['href'])
        except KeyError:
            pass
        except IndexError:
            pass

    return mp4_links


def scroll_to_bottom(driver):
    # Get scroll height
    last_height = driver.execute_script("return window.pageYOffset")

    count = 0
    while True:
        # Scroll down to bottom
        body = driver.find_element_by_tag_name('body')
        body.send_keys(Keys.PAGE_DOWN)

        __import__('time').sleep(2.5)

        new_height = driver.execute_script("return window.pageYOffset")

        if new_height == last_height:
            break

        last_height = new_height


def download_all(links):
    for title, link in links.items():
        print(f'\n[*] Starting download of the video: {title}')

        title = ''.join(e for e in title if e.isalnum() or e in (' ', '-', '_'))
        try:
            wget.download(link, f'f:\\metokur\\{title}.mp4')
        except Exception as ex:
            print(f'[*] Error -- {str(ex)}')


def main():
    driver = Driver()
    links = list(set(retrieve_video_links(driver)))

    print('[*] Scraping download links')
    dl_links = {}
    try:
        for link in links:
            driver.web_driver.get('https://bitchute.com' + link)
            soup = BeautifulSoup(driver.web_driver.page_source, 'html.parser')
            title = soup.select_one('#video-title').text

            try:
                dl_links[title] = soup.find('source').attrs['src']
            except Exception as ex:
                print(f'[*] Error -- {str(ex)}')

            __import__('time').sleep(2)
    finally:
        driver.close()

    download_all(dl_links)


main()
