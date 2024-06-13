from django import forms

DAYS = (
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miércoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    )

class ScheduleForm(forms.Form):
    title = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'required': True,'class':'form-control'}))
    text = forms.CharField(max_length=1000,widget=forms.Textarea(attrs={'required': True,'class':'form-control','rows':4,'cols':50}))
    week_days = forms.MultipleChoiceField(required=False,choices=DAYS,widget=forms.CheckboxSelectMultiple(attrs={'onchange':'disable_date()'}))
    day = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control','min': 1,'max': 31}))
    month = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control','min': 1,'max': 12}))
    time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'type': 'time', 'placeholder': 'HH:MM (DOB)','class': 'form-control'}))
    bot_message = forms.BooleanField(required=False)