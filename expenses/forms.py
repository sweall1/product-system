from django import forms
from .models import *



class ExpenseSearchForm(forms.ModelForm):
    GROPING = ('date',)
    grouping = forms.ChoiceField(choices=[('', '')] + list(zip(GROPING, GROPING)))
    start_date = forms.CharField(label='Date starts:', max_length=100)
    end_date = forms.CharField(label='Date ends:', max_length=100)
    choice_field = forms.ChoiceField(label='', widget=forms.RadioSelect, choices=[('1', 'Ascending'), ('2', 'Descending')])
    select = forms.ModelMultipleChoiceField(label='Category', widget=forms.CheckboxSelectMultiple, queryset=Category.objects.all())


    class Meta:
        model = Expense
        fields = ('name', 'category',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].required = False





