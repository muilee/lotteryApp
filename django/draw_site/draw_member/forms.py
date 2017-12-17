from django import forms

class DrawForm(forms.Form):
	GROUP_CHOICE = [("μ's", "μ's"), ("K-ON!", "K-ON!"), ("ALL", "（全）")]

	group = forms.ChoiceField(
		choices = GROUP_CHOICE,
		label='團隊名稱',
		label_suffix='：',
		widget=forms.RadioSelect,
		initial='ALL'
	)