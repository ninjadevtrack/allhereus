from django.forms import ModelForm, ModelChoiceField, IntegerField, NumberInput, TypedChoiceField
from .models import MyUser, CheckIn, Student


class CheckInForm(ModelForm):
    """Custom class to create/edit CheckIn"""

    success_score = IntegerField(widget=NumberInput(attrs={'type': 'range', 'step': '1', 'min': '0', 'max': '10'}))

    class Meta:
        model = CheckIn
        fields = ['date', 'teacher', 'student', 'status',
                  'mode', 'notify_school_admin', 'success_score',
                  'info_learned', 'info_better']

    def __init__(self, user, *args, **kwargs):
        super(CheckInForm, self).__init__(*args, **kwargs)
        self.fields['teacher'] = ModelChoiceField(queryset=MyUser.objects.filter(pk=user.id), empty_label=None)
        self.fields['student'] = ModelChoiceField(queryset=Student.objects.filter(teacher=user), empty_label=None)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        # remove the empty states for TypedChoiceField which is used by status
        # and mode.
        # see: https://stackoverflow.com/a/29429615/3720597
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, TypedChoiceField):
                field.choices = field.choices[1:]


class ProfileForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'school', 'department', 'first_name', 'last_name', 'subject', 'grade']
