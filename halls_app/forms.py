from django import forms

class HallForm(forms.Form):
    hall = forms.CharField(max_length=225)
    hall_capacity = forms.IntegerField()
    projector = forms.BooleanField(required=False)


class HallNameForm(forms.Form):
    hall = forms.CharField(max_length=225)

class HallCapacityForm(forms.Form):
    hall_capacity = forms.IntegerField()

class  ProjectorForm(forms.Form):
    projector = forms.BooleanField(required=False)

class ReserveForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput())
    comment = forms.CharField(widget=forms.Textarea)
