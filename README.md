# Job Search
A tool to help me find open developer positions in Toronto with a focus on companies rather than positions available.
It is based on the idea that the company's goals determine if I want to work there or not, and hopefully companies I am interested in need of someone with my skill set.

# Getting started
```
python manage.py migrate
python manage.py scrape
```

To view results:
```
python manage.py createsuperuser
python manage.py runserver
```
After that, login to the admin panel and view the results

Ignore results from companies you do not want to work for and continue to build more scrapers
