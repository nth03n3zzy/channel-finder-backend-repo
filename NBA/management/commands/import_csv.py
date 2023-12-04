import csv
from django.core.management.base import BaseCommand
from NBA.models import Schedule  # Import your Schedule model

# interestingly Command has to be written explicitly as command or django will have a problem.


class Command(BaseCommand):
    help = 'Import schedule data from CSV files'

    def handle(self, *args, **options):
        # List of CSV files to import
        csv_files = [
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/atl Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/bkn Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/bos Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/cha Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/chi Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/cle Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/dal Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/den Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/det Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/gs Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/hou Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/ind Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/lac Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/lal Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/mem Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/mia Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/mil Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/min Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/no Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/ny Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/okc Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/orl Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/phi Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/phx Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/por Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/sa Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/sac Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/tor Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/utah Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NBA_schedules/wsh Schedule 2023-2024.csv',

        ]
        # loop to go through all csv files.
        for csv_file in csv_files:
            # open csv files
            with open(csv_file, 'r') as file:
                # read csv files
                reader = csv.DictReader(file)
                # go through each row.
                for row in reader:
                    # Assuming CSV column names match your model fields
                    team = row['team']
                    # was having an issue  with team fields being blank. this tells the
                    #  usser on import that the team field is filled out
                    self.stdout.write(self.style.SUCCESS(
                        f'Read team from CSV: {team}'))
                    schedule = Schedule(
                        team=team,
                        date=row['date'],
                        opponent=row['opponent'],
                        time=row['time'],
                        channel=row['channel']
                    )
                    schedule.save()

            self.stdout.write(self.style.SUCCESS(
                f'Successfully imported data from {csv_file}'))
