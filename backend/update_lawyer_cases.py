import os, sys, django
sys.path.append('/Users/sin/Downloads/LIT/backend')
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"
django.setup()
from chatmiddleware.models import Lawyer
from chatmiddleware.lawnet import search, retrieve_case


def get_search_cases(name):
    root = search(name)
    citations = []
    for child in root.iter():
        if child.tag == 'Citation':
            if child.text: citations.append(child.text)
    return citations


if __name__ == '__main__':
    lawyers = Lawyer.objects.all()
    for lawyer in lawyers:
        name = lawyer.name
        case_list = get_search_cases(name)
        lawyer.cases = '|'.join(case_list)
        lawyer.save()
