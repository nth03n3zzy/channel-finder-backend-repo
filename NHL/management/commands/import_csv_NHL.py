import csv
from django.core.management.base import BaseCommand
from NHL.models import Schedule  # Import your Schedule model

# interestingly Command has to be written explicitly as command or django will have a problem.


class Command(BaseCommand):
    help = 'Import schedule data from CSV files'

    def handle(self, *args, **options):

        # List of CSV files to import
        csv_files = [
            './web_scraping_code/NHL_schedules/ana Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/ari Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/bos Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/buf Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/car Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/cbj Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/cgy Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/chi Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/col Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/dal Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/det Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/edm Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/fla Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/la Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/min Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/mtl Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/nj Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/nsh Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/nyi Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/nyr Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/ott Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/phi Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/pit Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/sea Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/sj Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/stl Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/tb Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/tor Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/van Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/vgk Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/wpg Schedule 2023-2024.csv',
            './web_scraping_code/NHL_schedules/wsh Schedule 2023-2024.csv'
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
