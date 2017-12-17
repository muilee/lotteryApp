import csv

with open("draw_member/members.csv", "r") as f:
	csv_reader = csv.DictReader(f)
	members = [(row['名字'], row['團體']) for row in csv_reader]

from draw_member.models import Member

for member in members:
	Member(name=member[0], group_name=member[1]).save()

# python manage.py dumpdata --format=yaml --indent=4 --output draw_member/fixtures/anime_members.yaml draw_member.Member