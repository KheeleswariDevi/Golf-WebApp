from django import forms
from .models import Golfer, GolfCourse
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, DecimalValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class AddGolferForm(forms.Form):
    '''The form for adding a new golfer.'''

    forename = forms.CharField(validators=[MaxLengthValidator(50)])
    surname = forms.CharField(validators=[MaxLengthValidator(50)])
    handicap = forms.IntegerField(validators=[MaxValueValidator(54)])


class AddGolfCourseForm(forms.Form):
    '''The form for adding a new golf course.'''

    name = forms.CharField(validators=[MaxLengthValidator(50)])
    latitude = forms.DecimalField(
        help_text='(optional)',
        required=False,
        validators=[MinValueValidator(-90), MaxValueValidator(90), DecimalValidator(max_digits=5, decimal_places=3)])

    longitude = forms.DecimalField(
        help_text = '(optional)',
        required=False,
        validators=[MinValueValidator(-180), MaxValueValidator(180), DecimalValidator(max_digits=6, decimal_places=3)])
