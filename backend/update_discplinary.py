import os, sys, django
sys.path.append('/Users/sin/Downloads/LIT/backend')
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"
django.setup()
from chatmiddleware.lawnet import search, retrieve_case
from chatmiddleware.models import Lawyer

keys = ['law', 'society', 'singapore', 'disciplinary', 'procedure', 'legal', 'profession']

lawyers = Lawyer.objects.all()

for lawyer in lawyers:
    search_results_tree = search(' '.join(keys + [lawyer.name]))
    disciplinary_flag = False
    for el in search_results_tree.iter():
        if el.tag == 'Title' and lawyer.name.lower() in el.text.lower():
            disciplinary_flag = True
            break
    if disciplinary_flag:
        lawyer.disciplinary_fault = True
        lawyer.save()
