from url_list import Url
from datetime import datetime, timedelta
from game import Game
import requests
from bs4 import BeautifulSoup
import sys
import pytz
from datetime import datetime, date, time
sys.path.append('/Users/daddy/Desktop/web_scraper_NBA/channel-finder/back-end')

# ADD FUNCTIONALITY FOR HOME OR AWAY
# tester url not used when csvs are actually created urls are used from url_list.py
url = "https://www.espn.com/nfl/team/schedule/_/name/ari/arizona-cardinals"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

page = requests.get(url, headers=headers)

doc = BeautifulSoup(page.text, "html.parser")

# Find all rows with class "Table__TR--sm" row 0 is the heading for the table so it will need to be skipped.
oddRows = doc.find_all('tr', class_='Table__TR Table__TR--sm Table__even')[2]

evenRows = doc.find_all(
    'tr', class_='filled Table__TR Table__TR--sm Table__even')[5]

# function to find the date contained in the row that is being inputted.

# function to pull the name of nba teams from espns nba urls


def get_team_name(url):
    name_list = url.split('/')[-3]
    name = name_list.replace('-', ' ')
    return name

# function to get name of nhl teams from espns nhl urls


def get_team_name_nhl(url):
    name_list = url.split('/')[-2]
    name = name_list.replace('-', ' ')
    return name

# function works for nba and nhl


def find_date(row):

    # date of games is found in the first span tag.
    date = row.find("span").text

    return date


def find_date_nfl(row):

    # date of games is found in
    date_row = row.find_all('td', class_='Table__TD')[1]
    if date_row.find('span'):
        date = date_row.find('span').text
        return date

    return 'BYE WEEK'

# function to find the opponent contained in the row being searcehd.


def find_opponent(row):

    # opponent title is dound in a anchor tab
    opponent_element = row.find_next('a', tabindex='0')

    # the name is contained in the href for this anchor tab this is an example of the print out
    # "/nba/team/_/name/ny/new-york-knicks"
    opponent_href = opponent_element['href']

    # .split('/') seperates the string into a list each element corresponding to where the
    # slash is ['', 'nba', 'team', '_','name','ny','new-york-knicks']. the [-1] tells the
    # split to grab the last item in the list reverse indexing in python -1 is the last
    # item -2 is the second to last item and so forth.
    team_name_abbreviation = opponent_href.split('/')[-1]

    # replacing all '-' with ' ' so the team name looks like a normal team name. "new york knicks"
    team_name = team_name_abbreviation.replace('-', ' ')

    return team_name

# function to find the game time of the row entered.
# the following code is added so that the string that is pulled from ESPN is converted to a date time object
# that date time object is converted from EST to UTC and then back to a string
# on the front end the UTC string will be converted to a timeObject which will be in the users time Zone


def find_time(row, scraped_date):

    time_element = row.find_all('td', class_='Table__TD')[2]
    time_est = time_element.text.strip()

    time_parts = time_est.split()
    if len(time_parts) != 2 or not time_parts[0].count(':') == 1:
        return 'invalid time'

    # Include the day of the month in the date string
    date_str = scraped_date + f' {datetime.now().year}'

    # Split the date string
    date_parts = date_str.split(', ')
    date_part_day_of_week = date_parts[0].strip()
    date_part_month, date_part_day_of_month, date_part_year = date_parts[1].split(
        ' ')

    # Get the current date.
    current_date = date.today()

    # handling for the date of feb 29th as that is a leap year date.
    if date_part_month == 'Feb' and date_part_day_of_month == '29':
        year = 2024
        scraped_date = datetime.strptime(
            f'{year} {date_part_month} {date_part_day_of_month}', '%Y %b %d'
        )
    # if the date is not feb 29th we compare the date to todays date the date of th scraping
    # if the date is less than the current date the date is assumed to be next year as that
    # will have already passed and cant be for the current year.
    else:
        scraped_date = datetime.strptime(
            f'{date_part_month} {date_part_day_of_month}', '%b %d')
        # Check if the game is in the next year (2024) or current year (2023)
        if (scraped_date.month, scraped_date.day) < (current_date.month, current_date.day):
            # Assume the game is in the next year (2024)
            year = current_date.year + 1
        else:
            year = current_date.year  # Assume the game is in the current year

    # Create the correct date for the game using the determined year
    date_obj = datetime(year, scraped_date.month, scraped_date.day)

    # handling for changing the time from a 12hr format to a 24 hour format and then conversion to UTC from EST
    time_parts = time_est.split()
    time_hour, time_minute = map(int, time_parts[0].split(':'))
    # as well hanfling for the hour 12pm as the time 2400 isnt correct
    if time_parts[1].lower() == 'pm' and time_hour != 12:
        time_hour += 12
    time_est = time(hour=time_hour, minute=time_minute)

    est_datetime_object = datetime.combine(date_obj, time_est)

    est_timezone = pytz.timezone('US/Eastern')
    est_datetime_object = est_timezone.localize(est_datetime_object)
    utc_datetime_object = est_datetime_object.astimezone(pytz.utc)

    utc_datetime_string = utc_datetime_object.strftime('%Y-%m-%d %H:%M:%S')

    return utc_datetime_string

# seperate find time function for the nfl due to the schedule being formatted different.


def find_time_nfl(row, scraped_date):
    if scraped_date == 'BYE WEEK':
        return 'BYE WEEK'

    time_element = row.find_all('td', class_='Table__TD')[3]
    time_est = time_element.text.strip()

    if time_est == 'TBD':
        return 'TBD'

    time_parts = time_est.split()
    if len(time_parts) != 2 or not time_parts[0].count(':') == 1 and time_parts != 'TBD':
        return 'invalid time'

    # Include the day of the month in the date string
    date_str = scraped_date + f' {datetime.now().year}'

    # Split the date string
    date_parts = date_str.split(', ')
    date_part_day_of_week = date_parts[0].strip()
    date_part_month, date_part_day_of_month, date_part_year = date_parts[1].split(
        ' ')

    # Get the current date.
    current_date = date.today()

    # handling for the date of feb 29th as that is a leap year date.
    if date_part_month == 'Feb' and date_part_day_of_month == '29':
        year = 2024
        scraped_date = datetime.strptime(
            f'{year} {date_part_month} {date_part_day_of_month}', '%Y %b %d'
        )
    # if the date is not feb 29th we compare the date to todays date the date of th scraping
    # if the date is less than the current date the date is assumed to be next year as that
    # will have already passed and cant be for the current year.
    else:
        scraped_date = datetime.strptime(
            f'{date_part_month} {date_part_day_of_month}', '%b %d')
        # Check if the game is in the next year (2024) or current year (2023)
        if (scraped_date.month, scraped_date.day) < (current_date.month, current_date.day):
            # Assume the game is in the next year (2024)
            year = current_date.year + 1
        else:
            year = current_date.year  # Assume the game is in the current year

    # Create the correct date for the game using the determined year
    date_obj = datetime(year, scraped_date.month, scraped_date.day)

    # handling for changing the time from a 12hr format to a 24 hour format and then conversion to UTC from EST
    time_parts = time_est.split()
    time_hour, time_minute = map(int, time_parts[0].split(':'))
    # as well hanfling for the hour 12pm as the time 2400 isnt correct
    if time_parts[1].lower() == 'pm' and time_hour != 12:
        time_hour += 12
    time_est = time(hour=time_hour, minute=time_minute)

    est_datetime_object = datetime.combine(date_obj, time_est)

    est_timezone = pytz.timezone('US/Eastern')
    est_datetime_object = est_timezone.localize(est_datetime_object)
    utc_datetime_object = est_datetime_object.astimezone(pytz.utc)

    utc_datetime_string = utc_datetime_object.strftime('%Y-%m-%d %H:%M:%S')

    return utc_datetime_string

# function to find what channel the game is on.
# def find_channel(row):


def find_channel_nfl(row):

    length = len(row.find_all('td', class_='Table__TD'))

    if len(row.find_all('td', class_='Table__TD')) == 2:
        return 'BYE WEEK'
    channel_element = row.find_all('td', class_='Table__TD')[4]
    channel_list = []

    if channel_element.find('div', class_='network-container'):

        if channel_element.find('figure'):

            channel_figures = channel_element.find_all('figure')

            for figure in channel_figures:
                # grabs the last element from the class tag channel_long will look like "network-'netwrok name such as espn'""
                channel_long = figure['class'][-1]
                # removes the hifen so chanel_break = ['network','espn'].
                channel_break = channel_long.split('-')
                # we grab the last element channel = 'espn'.
                channel = channel_break[-1]
                # we add the channel to the channel list.
                channel_list.append(channel)

        if channel_element.find('a'):

            channel_figures = channel_element.find_all('a')

            for figure in channel_figures:
                # Extract the string from the 'href' attribute
                channel_href = figure['href']
                if channel_href == 'http://www.espn.com/watch/espnplus':
                    channel_list.append('ESPN+')
                if channel_href == 'https://www.hulu.com':
                    channel_list.append('HULU')

            return channel_list

        channel = channel_element.find('div').text
        return channel

    channel = 'TBD'
    return channel


def find_channel_nhl(row):
    channel_element = row.find_all('td', class_='Table__TD')[3]
    channel_list = []

    if channel_element.find('div', class_='network-container'):

        if channel_element.find('figure'):

            channel_figures = channel_element.find_all('figure')

            for figure in channel_figures:
                # grabs the last element from the class tag channel_long will look like "network-'netwrok name such as espn'""
                channel_long = figure['class'][-1]
                # removes the hifen so chanel_break = ['network','espn'].
                channel_break = channel_long.split('-')
                # we grab the last element channel = 'espn'.
                channel = channel_break[-1]
                # we add the channel to the channel list.
                channel_list.append(channel)

        if channel_element.find('a'):

            channel_figures = channel_element.find_all('a')

            for figure in channel_figures:
                # Extract the string from the 'href' attribute
                channel_href = figure['href']
                if channel_href == 'http://www.espn.com/watch/espnplus':
                    channel_list.append('ESPN+')
                if channel_href == 'https://www.hulu.com':
                    channel_list.append('HULU')

            return channel_list

        channel = channel_element.find('div').text
        return channel

    channel = 'NHL CENTER ICE'
    return channel


def find_channel(row):

    # takes us to the table data tag that contains channel information.
    channel_element = row.find_all('td', class_='Table__TD')[3]

    # checks if there is a div tag with the class network container
    if channel_element.find('div', class_='network-container'):
        # check if there is a figure tag nested within
        if channel_element.find('figure'):

            channel_figures = channel_element.find_all(
                'figure')  # Find all figure tags

            # List to store channel information since there can be more than one channel
            channel_list = []

            # for loop that will iterate through all the figure tags
            for figure in channel_figures:
                # grabs the last element from the class tag channel_long will look like "network-'netwrok name such as espn'""
                channel_long = figure['class'][-1]
                # removes the hifen so chanel_break = ['network','espn'].
                channel_break = channel_long.split('-')
                # we grab the last element channel = 'espn'.
                channel = channel_break[-1]
                # we add the channel to the channel list.
                channel_list.append(channel)

            return channel_list  # channel list is returned.

        # if the div tag does not have a figure than the channel is in the text of the div tag.
        channel = channel_element.find('div').text
        return channel

    channel = "NBA League Pass"
    return channel


def get_schedule(tag, class_odd_rows, class_even_rows, url):

    # sets header for scrapper so queries appear to come from a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    # page data requests.get
    page = requests.get(url, headers=headers)

    # parsing doc
    doc = BeautifulSoup(page.text, "html.parser")

    # finding all the data for all odd rows
    oddrows = doc.find_all(tag, class_=class_odd_rows)

    # finding the data for all even rows cause they have a seperate tag
    evenrows = doc.find_all(tag, class_=class_even_rows)

    # for some reason the person who did the front end for espn gave the last row a sepereate class name.
    lastrow = doc.find_all(
        tag, 'filled bb--none Table__TR Table__TR--sm Table__even')[0]

    schedule_data = []

    # min length calculated for looping and printing logic because the number of even and odd rows are not the same
    # but we alternate between even and odd so we need to know at what index to stop getting info from the shorter list
    # so that we dont get an index out of bounds error.
    min_length = min(len(oddrows), len(evenrows))

    # for loop alternating between even and odd rows. first odd row is skipped because it jsut contains header information

    for r, n in enumerate(range(min_length), start=1):

        game = Game(get_team_name(url), find_date(oddrows[r]), find_opponent(
            oddrows[r]), find_time(oddrows[r], find_date(oddrows[r])), find_channel(oddrows[r]))

        data_dictionary = {'team': game.team,
                           'date': game.date,
                           'opponent': game.opponent,
                           'time': game.time,
                           'channel': game.channel}

        schedule_data.append(data_dictionary)

        game = Game(get_team_name(url), find_date(evenrows[n]), find_opponent(
            evenrows[n]), find_time(evenrows[n], find_date(evenrows[n])), find_channel(evenrows[n]))

        data_dictionary = {'team': game.team,
                           'date': game.date,
                           'opponent': game.opponent,
                           'time': game.time,
                           'channel': game.channel}

        schedule_data.append(data_dictionary)

    # since we stop printing after min length we need to print the last odd row

    game = Game(get_team_name(url), find_date(oddrows[40]), find_opponent(
        oddrows[40]), find_time(oddrows[40], find_date(oddrows[40])), find_channel(oddrows[40]))

    data_dictionary = {'team': game.team,
                       'date': game.date,
                       'opponent': game.opponent,
                       'time': game.time,
                       'channel': game.channel}

    schedule_data.append(data_dictionary)

    # and since they gave the last row a different class we also have seperate print commands for that.
    game = Game(get_team_name(url), find_date(lastrow), find_opponent(lastrow),
                find_time(lastrow, find_date(lastrow)), find_channel(lastrow))

    data_dictionary = {'team': game.team,
                       'date': game.date,
                       'opponent': game.opponent,
                       'time': game.time,
                       'channel': game.channel}

    schedule_data.append(data_dictionary)

    return schedule_data


def get_schedule_nfl(tag, class_odd_rows, class_even_rows, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    # page data requests.get
    page = requests.get(url, headers=headers)

    # parsing doc
    doc = BeautifulSoup(page.text, "html.parser")

    # finding all the data for all odd rows
    oddrows = doc.find_all(tag, class_=class_odd_rows)

    # finding the data for all even rows cause they have a seperate tag
    evenrows = doc.find_all(tag, class_=class_even_rows)

    # for some reason the person who did the front end for espn gave the last row a sepereate class name.
    try:
        lastrow = doc.find_all(
            tag, 'bb--none Table__TR Table__TR--sm Table__even')[1]

    except Exception:
        length = len(doc.find_all(
            tag, 'filled bb--none Table__TR Table__TR--sm Table__even'))
        lastrow = doc.find_all(
            tag, 'filled bb--none Table__TR Table__TR--sm Table__even')[1]

    schedule_data = []

    min_length = min(len(oddrows), len(evenrows))

    for r, n in enumerate(range(min_length), start=1):

        game = Game(get_team_name_nhl(url), find_date_nfl(oddrows[r]), find_opponent(
            oddrows[r]), find_time_nfl(oddrows[r], find_date_nfl(oddrows[r])), find_channel_nfl(oddrows[r]))

        if game.date == 'DATE':
            continue

        data_dictionary = {'team': game.team,
                           'date': game.date,
                           'opponent': game.opponent,
                           'time': game.time,
                           'channel': game.channel}

        schedule_data.append(data_dictionary)

        game = Game(get_team_name_nhl(url), find_date_nfl(evenrows[n]), find_opponent(
            evenrows[n]), find_time_nfl(evenrows[n], find_date_nfl(evenrows[n])), find_channel_nfl(evenrows[n]))

        if game.date == 'DATE':
            continue

        data_dictionary = {'team': game.team,
                           'date': game.date,
                           'opponent': game.opponent,
                           'time': game.time,
                           'channel': game.channel}

        schedule_data.append(data_dictionary)

    game = Game(get_team_name_nhl(url), find_date_nfl(evenrows[7]), find_opponent(
        evenrows[7]), find_time_nfl(evenrows[7], find_date_nfl(evenrows[7])), find_channel_nfl(evenrows[7]))

    data_dictionary = {'team': game.team,
                       'date': game.date,
                       'opponent': game.opponent,
                       'time': game.time,
                       'channel': game.channel}

    schedule_data.append(data_dictionary)

    game = Game(get_team_name_nhl(url), find_date_nfl(lastrow), find_opponent(
        lastrow), find_time_nfl(lastrow, find_date_nfl(lastrow)), find_channel_nfl(lastrow))

    data_dictionary = {'team': game.team,
                       'date': game.date,
                       'opponent': game.opponent,
                       'time': game.time,
                       'channel': game.channel}

    schedule_data.append(data_dictionary)

    return schedule_data


def get_schedule_nhl(tag, class_odd_rows, class_even_rows, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    # page data requests.get
    page = requests.get(url, headers=headers)

    # parsing doc
    doc = BeautifulSoup(page.text, "html.parser")

    # finding all the data for all odd rows
    oddrows = doc.find_all(tag, class_=class_odd_rows)

    # finding the data for all even rows cause they have a seperate tag
    evenrows = doc.find_all(tag, class_=class_even_rows)

    # for some reason the person who did the front end for espn gave the last row a sepereate class name.
    try:
        lastrow = doc.find_all(
            tag, 'bb--none Table__TR Table__TR--sm Table__even')[1]

    except Exception:
        lastrow = doc.find_all(
            tag, 'filled bb--none Table__TR Table__TR--sm Table__even')[1]

    schedule_data = []

    min_length = min(len(oddrows), len(evenrows))

    for r, n in enumerate(range(min_length), start=1):

        game = Game(get_team_name_nhl(url), find_date(oddrows[r]), find_opponent(
            oddrows[r]), find_time(oddrows[r], find_date(oddrows[r])), find_channel_nhl(oddrows[r]))

        data_dictionary = {'team': game.team,
                           'date': game.date,
                           'opponent': game.opponent,
                           'time': game.time,
                           'channel': game.channel}

        schedule_data.append(data_dictionary)

        game = Game(get_team_name_nhl(url), find_date(evenrows[n]), find_opponent(
            evenrows[n]), find_time(evenrows[n], find_date(evenrows[n])), find_channel_nhl(evenrows[n]))

        data_dictionary = {'team': game.team,
                           'date': game.date,
                           'opponent': game.opponent,
                           'time': game.time,
                           'channel': game.channel}

        schedule_data.append(data_dictionary)

    game = Game(get_team_name_nhl(url), find_date(oddrows[41]), find_opponent(
        oddrows[41]), find_time(oddrows[41], find_date(oddrows[41])), find_channel_nhl(oddrows[41]))

    data_dictionary = {'team': game.team,
                       'date': game.date,
                       'opponent': game.opponent,
                       'time': game.time,
                       'channel': game.channel}

    schedule_data.append(data_dictionary)

    game = Game(get_team_name_nhl(url), find_date(lastrow), find_opponent(
        lastrow), find_time(lastrow, find_date(lastrow)), find_channel_nhl(lastrow))

    data_dictionary = {'team': game.team,
                       'date': game.date,
                       'opponent': game.opponent,
                       'time': game.time,
                       'channel': game.channel}

    schedule_data.append(data_dictionary)

    return schedule_data


urls = Url.nba_url_list

print(get_schedule_nfl('tr', 'Table__TR Table__TR--sm Table__even',
                       'filled Table__TR Table__TR--sm Table__even', url))

# print(find_date_nfl(oddRows))
# print(find_opponent(oddRows))
#print(find_time_nfl(evenRows, find_date_nfl(evenRows)))
# print(find_channel_nfl(evenRows))
