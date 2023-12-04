import csv
from django.core.management.base import BaseCommand
from NFL.models import Schedule  # Import your Schedule model

# interestingly Command has to be written explicitly as command or django will have a problem.


class Command(BaseCommand):
    help = 'Import schedule data from CSV files'

    def handle(self, *args, **options):
        # List of CSV files to import
        csv_files = [
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/ari Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/atl Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/bal Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/buf Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/car Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/chi Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/cin Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/cle Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/dal Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/den Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/det Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/gb Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/hou Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/ind Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/jax Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/kc Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/lac Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/lar Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/lv Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/mia Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/min Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/ne Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/no Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/nyg Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/nyj Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/phi Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/pit Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/sea Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/sf Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/tb Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/ten Schedule 2023-2024.csv',
            '/Users/daddy/Desktop/web_scraper_NBA/backend/web_scraping_code/NFL_schedules/wsh Schedule 2023-2024.csv'
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
