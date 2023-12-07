import web_scraping
from url_list import Url
import csv
import time
import requests
# this one is for NBA  and refractoring in VS code sucks or i am dumb so it isnt tagged as such


def create_csv(url):
    # pulls the team abbreviation from the url
    csv_file_team = url.split('/')[-3]

    csv_file_name = f"{csv_file_team} Schedule 2023-2024.csv"

    data = web_scraping.get_schedule('tr', 'Table__TR Table__TR--sm Table__even',
                                     'filled Table__TR Table__TR--sm Table__even', url)

    # fields names
    field_names = ['team', 'date', 'opponent', 'time', 'channel']

    # Write the data to the CSV file
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()  # Write the header row
        writer.writerows(data)  # Write the data rows


def create_csv_nfl(url):
    # pulls the team abbreviation from the url
    csv_file_team = url.split('/')[-2]

    csv_file_name = f"{csv_file_team} Schedule 2023-2024.csv"

    data = web_scraping.get_schedule_nfl('tr', 'Table__TR Table__TR--sm Table__even',
                                         'filled Table__TR Table__TR--sm Table__even', url)

    # fields names
    field_names = ['team', 'date', 'opponent', 'time', 'channel']

    # Write the data to the CSV file
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()  # Write the header row
        writer.writerows(data)  # Write the data rows


def create_csv_nhl(url):
    # pulls the team abbreviation from the url
    csv_file_team = url.split('/')[-2]

    csv_file_name = f"{csv_file_team} Schedule 2023-2024.csv"

    data = web_scraping.get_schedule_nhl('tr', 'Table__TR Table__TR--sm Table__even',
                                         'filled Table__TR Table__TR--sm Table__even', url)

    # fields names
    field_names = ['team', 'date', 'opponent', 'time', 'channel']

    # Write the data to the CSV file
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()  # Write the header row
        writer.writerows(data)  # Write the data rows


# LIST OF ALL TEAM URLS  TO BE ITERATED THROUGH
urls_nba = Url.nba_url_list
urls_nhl = Url.nhl_url_list
urls_nfl = Url.nfl_url_list

# loop creates a csv file for each team and their schedule.
for i in range(len(urls_nba)):
    # try:
    create_csv(urls_nba[i])
    # except Exception as e:
    #    print(f"Error while processing {urls_nba[i]}: {str(e)}")
