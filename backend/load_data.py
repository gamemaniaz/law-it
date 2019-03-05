import os, sys, django
sys.path.append('/Users/sin/Downloads/LIT/backend')
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"
django.setup()
from chatmiddleware.models import Lawyer
import datetime


with open('data.csv') as f:
    f.readline()
    for line in f:
        parts = line.split(',')
        date = datetime.datetime.strptime(parts[4], '%d/%m/%Y').strftime('%Y-%m-%d') if parts[4] != '' else None
        lawyer = Lawyer(
            name=parts[0],
            job_title=parts[1],
            key_practice_areas=parts[2],
            law_prac_name=parts[3],
            admission_date=date,
            law_prac_type=parts[5],
            email=parts[6],
            website=parts[7],
            tel=parts[8],
            address=parts[9]
        )
        lawyer.save()
