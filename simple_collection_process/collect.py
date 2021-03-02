from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv

""" This program parse top k ariticles informaiton from hedgeye.com

publish_date (datetime): <time class="article__time" datetime="2021-02-26T11:24:50-05:00"
headline = "" # <h1 class="article__header se-headline"
author_name = "" #<div class="full-name"> Name </div>
author_image_url = "" # <div class="headshot"> <img alt="Headshot nhowe" src="urlA"> </div>
author_twitter_handle = "" #<div class="twitter-handle"> <a href="url"> @abcd </a> </div>
author_twitter_url = "" #<div class="twitter-handle"> <a href="url"> @abcd </a> </div>
first_image_url = "" # <a class="cboxElement" href = "url">
"""


base = 'https://app.hedgeye.com'
url = base + '/insights/archives/?month=2021-02-01&type=insights'

article_class = 'thumbnail-article-quarter'
article_link_class = "thumbnail-article-quarter__title-link"
output_csv_file = 'output.csv'

resp = requests.get(url)

soup = BeautifulSoup(resp.text, 'lxml')

i = 0
max_runs = 10
results =[]
header=['publishDate', 'headline', 'first_mg_url', 'headshot_url', 'author_name', 'twitter_url', 'twitter_handle']

for article_div in soup.find_all('div', {'class':article_class}):
    print(f'Getting article {(i+1)} ...', end = ' ')
    # use header count to put value in the correct key based on header list
    header_count = 0

    href = article_div.find('a').get('href')
    href = base + href
    #print(href)

    # request the article
    article_resp = requests.get(href)
    # get the article soup
    #a_soup = BeautifulSoup(article_resp.text, 'lxml') # article soup
    if article_resp is None:
        continue

    # parse necessary info into a dictionary
    item_dict = {}
    #item_dict['html_body'] = article_resp.text

    a_soup = BeautifulSoup(article_resp.text, 'lxml') # article soup

    #publish date
    date_soup = a_soup.find("time", {'class':'article__time'})

    publish_date = None
    if date_soup is not None:
        publish_date = date_soup.get('datetime')
        item_dict['publishDate'] = publish_date
    header_count += 1
    #print(publish_date)

    # headline
    headline_soup = a_soup.find('h1', {'class': 'article__header'})
    item_dict['headline'] = (headline_soup.text).strip()
    header_count += 1
    #print(headline_soup.text)

    # firs image
    first_img_soup = a_soup.find('a', {'class': 'cboxElement'})
    first_img_url = None
    if first_img_soup is not None:
        first_img_url = first_img_soup.get('href')
        #print(first_img_url)
        item_dict['first_img_url'] = first_img_url
    header_count += 1

    #author image url
    headshot = a_soup.find("div", class_="headshot")
    if headshot is not None:
        # if there is the author section
        #print(headshot.img.get('src'))
        headshot_url = headshot.img.get('src')
        item_dict['headshot_url'] = headshot_url
        header_count += 1
        #author name
        author_name = a_soup.find("div", {'class':'full-name'}).text
        item_dict['author_name'] = author_name
        header_count += 1
        #print(author_name)

        # twitter handle
        tw_handle = a_soup.find("div", {'class':'twitter-handle'}).a
        twitter_url = tw_handle.get('href')
        item_dict['twitter_url'] = twitter_url
        header_count += 1
        twitter_handle = tw_handle.text
        item_dict['twitter_handle'] = twitter_handle

    #print('===========================')
    print(' Done.')

    # Add dictionary into the result list
    results.append(item_dict)
    i = i + 1
    if i == max_runs:
        break

with open(output_csv_file, 'w') as f:
    dict_writer = csv.DictWriter(f, header)
    dict_writer.writeheader()
    dict_writer.writerows(results)

