from django import forms

from hi_hike_hiking.hhhapp.models import Hike

class DateInput(forms.DateInput):
    input_type ='date'


# class ImageForm(forms.ModelForm):
#     class Meta:
#         model=Hike
#         fields=['image']
