from django.forms import ModelForm, ModelChoiceField, RadioSelect, IntegerField, NumberInput
from .models import MyUser, CheckIn, Student


class CheckInForm(ModelForm):
    """Custom class to create/edit CheckIn"""

    success_score = IntegerField(widget=NumberInput(attrs={'type': 'range', 'step': '1', 'min': '0', 'max': '10'}))

    class Meta:
        model = CheckIn
        fields = ['date', 'teacher', 'student', 'status',
                  'mode', 'notify_school_admin', 'success_score',
                  'info_learned', 'info_better']
        widgets = {field: RadioSelect() for field in ['mode', 'status']}

    def __init__(self, user, *args, **kwargs):
        super(CheckInForm, self).__init__(*args, **kwargs)
        self.fields['teacher'] = ModelChoiceField(queryset=MyUser.objects.filter(pk=user.id))
        self.fields['student'] = ModelChoiceField(queryset=Student.objects.filter(teacher=user))
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProfileForm(ModelForm):
    # email = EmailField(label='Email', max_length=255)
    # schools = MultipleChoiceField(label='Schools')
    # department = CharField(label='Department')
    class Meta:
        model = MyUser
        fields = ['email', 'school', 'department']
