import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import EVChargingLocation


class Command(BaseCommand):
    help = 'Load data from EV Station file'

    def handle(self, *args, **kwargs):
        data_file = settings.BASE_DIR / 'data' / 'ev-charging-stations-india.csv'
        keys = ('name', 'lattitude','longitude')  # the CSV columns we will gather data from.
        
        records = []
        with open(data_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append({k: row[k] for k in keys})

        # extract the latitude and longitude from the Point object
        for record in records:
            if record['lattitude'] != '' and record['longitude'] != '':
                record['lattitude'] = float(record['lattitude'])
                record['longitude'] = float(record['longitude'])
            
            # add the data to the database
                EVChargingLocation.objects.get_or_create(
                    staionName=record['name'],
                    latitude=record['lattitude'],
                    longitude=record['longitude']
                )
            else:
                print("Empty string found for latitude or longitude:", record)
            