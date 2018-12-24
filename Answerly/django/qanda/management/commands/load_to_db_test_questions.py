import csv

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from qanda.models import Question


class Command(BaseCommand):
    help = 'Load questions in db'

    def handle(self, *args, **kwargs):

        obj_lst = []

        # Admin user
        adm = User.objects.get(username='admin')

        with open('qanda/management/commands/data2.csv', 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                o = Question(
                    title=row[1][:120],
                    question=row[2],
                    user=adm
                )
                obj_lst.append(o)
                
        res = Question.objects.bulk_create(obj_lst)
        
        self.stdout.write(self.style.SUCCESS(
            'Successfully loaded all questions into db'
        ))