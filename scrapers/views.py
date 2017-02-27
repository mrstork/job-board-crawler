import time
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from .models import Company, Position

def save_or_skip(position_url, position_title, company_name):
    # do not feel qualified for senior roles yet
    if 'senior' in position_title.lower():
        return

    company, created = Company.objects.get_or_create(name=company_name)

    if company.ignored:
        return

    Position.objects.create(
        name=position_title,
        company=company,
        url=position_url,
    )

    print(company_name, '::', position_title)


def techvibes():
    page = 1
    total_pages = -1

    while page != total_pages + 1:
        url = 'https://jobs.techvibes.com/?status&department=development&location=Toronto&search_string&page={0}'.format(page)
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        total_pages = len(soup.find('ul', 'pagination').find_all('li', 'number'))
        listings = soup.find('div', 'listings').find_all('div', 'col-sm-6 col-xs-9')

        for listing in listings:
            position_url = listing.find('a').attrs['href']
            position_title = listing.find('h3').text.strip()
            company_name = listing.find('h5').text.strip()

            save_or_skip(position_url, position_title, company_name)

        page = page + 1

        # delays for 5 seconds between pages
        time.sleep(5)

def stackoverflow():
    url = 'http://stackoverflow.com/jobs/feed?l=Toronto%2c+ON%2c+Canada&d=19&u=Km'
    print(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')

    for listing in soup.find_all('item'):
        position_url = listing.find('link').contents[0].strip()
        position_title = listing.find('title').contents[0].strip()
        company_name = listing.find('name').contents[0].strip()
        save_or_skip(position_url, position_title, company_name)

def marsdd():
    # can only filter by one search tag at a time
    tags = ['development', 'engineering']

    for tag in tags:

        page = 1
        total_pages = -1

        while page != int(total_pages) + 1:
            url = 'https://www.marsdd.com/careers/page/{0}/?object_type=career&filters%5Bposts%5D%5Bcareer-industries%5D%5B%5D={1}&type=community_careers&s=Toronto%2C+ON'.format(page, tag)
            print(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Mars filters each page down based on your query, doesn't actually
            # change the list of responses so when there are no results that match
            # the set filters on the page the response is a 404 even if there may be
            # more results on the next page
            if response.status_code == 404:
                page = page + 1
                continue

            total_pages = soup.find('ul', 'pagination').find('li', 'inline').text.split(' ')[-1]
            listings = soup.find_all('div', 'page-body page-body--split inline-career')

            for listing in listings:
                position_url = listing.find('h5', 'career-title').find('a').attrs['href']
                position_title = listing.find('h5', 'career-title').text.strip()
                company_name = listing.find('h5', 'career-company').text.strip()

                save_or_skip(position_url, position_title, company_name)

            page = page + 1

            # delays for 5 seconds between pages
            time.sleep(5)

# Future targets
# https://jobs.github.com/positions?description=&location=Toronto
