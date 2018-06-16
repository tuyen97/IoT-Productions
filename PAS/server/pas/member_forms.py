from django import forms
from .models import Member


def add_attrs(placeholder='', display=True):

    attrs =  {
        'class': 'form-control',
        'placeholder': placeholder
    }
    if not display:
        attrs['style'] = 'display: none;'
    return attrs


class AddMemberForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs=add_attrs('Enter name')))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs=add_attrs('Enter email')))
    course = forms.CharField(label='Course', widget=forms.TextInput(attrs=add_attrs('Enter course')))
    position = forms.ChoiceField(label='Position', choices=Member.POSITION_IN_LAB_CHOICES,
                                 widget=forms.Select(attrs={'class': ''}))
    coefficient = forms.IntegerField(label='Coefficient', widget=forms.TextInput(attrs=add_attrs('Enter coefficient')))
    research_about = forms.CharField(label='Research about', widget=forms.TextInput(attrs=add_attrs('Enter the topics')))
    card_id = forms.CharField(label='Card ID', widget=forms.TextInput(attrs=add_attrs('Enter card_id')))

    class Meta:
        model = Member
        fields = ['name', 'email', 'course', 'position', 'coefficient', 'research_about', 'card_id']
