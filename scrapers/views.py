import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from .models import Company, Position
import time

def techvibes():
    pages = 5 # relatively arbitrary
    for page in range(1, pages + 1):
        url = 'https://jobs.techvibes.com/page/{0}?search_string=development&geo=&location=Toronto&status=&department='.format(page)
        print(url)

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        listings = soup.find('div', 'listings').find_all('div', 'col-sm-6 col-xs-9')

        for listing in listings:
            position_url = listing.find('a').attrs['href']
            position_title = listing.find('h3').text.strip()
            company_name = listing.find('h5').text.strip()

            # do not feel qualified for senior roles yet
            if 'senior' in position_title.lower():
                continue

            company, created = Company.objects.get_or_create(name__iexact=company_name)

            if company.ignored:
                continue

            Position.objects.create(
                name=position_title,
                company=company,
                url=position_url,
            )

            print(company_name, '::', position_title)

        # delays for 5 seconds between pages
        time.sleep(5)

# Future targets
# http://stackoverflow.com/jobs?sort=i&l=Toronto%2C+ON%2C+Canada&d=20&u=Km
# https://jobs.github.com/positions?description=&location=Toronto
