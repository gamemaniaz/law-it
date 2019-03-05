from operator import itemgetter
from datetime import date, datetime


def relevance_generator(list_of_lawyers, area_of_law):
    """ generates relevance score for each lawyer """
    
    weight_aol = 0.3
    weight_xp = 0.15
    weight_freq = 0.15

    unsorted_list = []

    for lawyer in list_of_lawyers:

        if lawyer.admission_date:
            # assigning initial score of lawyer, based off area of law
            lawyer_aols = lawyer.key_practice_areas.split('|')
            if area_of_law in lawyer_aols:
                score = weight_aol
            else:
                score = 0

            # calculating the score of freq of court appearances + xp in law practice
            lawyer_cases = len(lawyer.cases.split("|"))
            today = date.today()
            admission = lawyer.admission_date
            lawyer_xp = today.year - admission.year - ((today.month, today.day) < (admission.month, admission.day))
            lawyer_xp_and_freq = weight_freq * lawyer_cases + weight_xp * lawyer_xp
            score += lawyer_xp_and_freq

            # lawyer_id = lawyer.id
            unsorted_list.append({
                'lawyer': lawyer,
                'score': score
            })

    sorted_list = sorted(unsorted_list, key = itemgetter('score'), reverse=True)

    return [s['lawyer'] for s in sorted_list]
