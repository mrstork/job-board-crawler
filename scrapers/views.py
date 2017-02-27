import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from .models import Company, Position
import time

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

# Future targets
# https://jobs.github.com/positions?description=&location=Toronto
