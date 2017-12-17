from django.shortcuts import render
from django.http import HttpResponse, Http404
import random
from django.views.decorators.http import require_GET
from .models import Member, History
from .forms import DrawForm


def home(request):
	form = DrawForm()
	return render(request, 'draw_member/home.html', locals())


@require_GET
def draw(request):

	# group_name = request.GET.get("group_name", "ALL")
	# if group_name == "ALL":
	# 	valid_members = Member.objects.all()
	# else:
	# 	valid_members = Member.objects.filter(group_name=group_name)

	# if not valid_members.exists():
	# 	raise Http404("No member in group {}".format(group_name))

	form = DrawForm(request.GET)
	if form.is_valid():
		group_name = form.cleaned_data["group"]
		if group_name == "ALL":
			valid_members = Member.objects.all()
		else:
			valid_members = Member.objects.filter(group_name=group_name)
	else:
		raise Http404("No member in group {}".format(group_name))


	lucky_member = random.choice(valid_members)
	draw_history = History(member=lucky_member)

	draw_history.save()
	return render(request, "draw_member/draw.html", locals())


def history(request):
	recent_histories = History.objects.order_by("-time").all()[:10]
	return render(request, "draw_member/history.html", locals())

