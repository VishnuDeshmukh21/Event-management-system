import os
import pandas as pd
from django.core.management.base import BaseCommand
from events.models import Event
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from datetime import datetime, time

class Command(BaseCommand):
    help = 'Import events from a CSV file'

    def handle(self, *args, **options):
        # Construct the path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'static', 'data.csv')
        
        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file_path)

            # Iterate over rows in the DataFrame
            for index, row in df.iterrows():
                try:
                    date = datetime.strptime(row['date'], '%d-%m-%Y').date()
        
                    # Extract hour, minute, and second from the time string
                    time_var=row['time']
                    time_var =datetime.strptime(time_var, "%H:%M:%S").time()
                    print(time_var)
        
                    # Create a time object using the extracted components                    # Create and save the event
                    Event.objects.create(
                        event_name=row['event_name'],
                        city_name=row['city_name'],
                        date=date,
                        time=time_var,
                        latitude=row['latitude'],
                        longitude=row['longitude']
                    )
                except (ValueError, KeyError) as e:
                    # Handle errors in parsing date, time, or missing fields
                    self.stderr.write(f"Error processing row {index + 1}: {e}")

            self.stdout.write(self.style.SUCCESS('Events imported successfully'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('CSV file not found'))
