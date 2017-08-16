from django.forms import ModelForm, ModelChoiceField, IntegerField, NumberInput, TypedChoiceField, ValidationError, HiddenInput
from .models import MyUser, CheckIn, Student, School, District


class CheckInForm(ModelForm):
    """Custom class to create/edit CheckIn"""

    success_score = IntegerField(widget=NumberInput(attrs={'type': 'range', 'step': '1', 'min': '0', 'max': '10'}))

    class Meta:
        model = CheckIn
        fields = ['date', 'teacher', 'student', 'status',
                  'mode', 'notify_school_admin', 'success_score',
                  'info_learned', 'info_better']

    def clean(self):
        cleaned_data = super(CheckInForm, self).clean()
        teacher = cleaned_data.get("teacher")
        student = cleaned_data.get("student")

        # Basic validation of relationships
        # We should enforce this more on the model side
        if self.user.is_district_admin:
            if teacher.district != self.user.district or student.district != self.user.district:
                raise ValidationError("Teacher/student districts must match.")
        elif self.user.is_school_admin:
            if teacher.school != self.user.school or student.school != self.user.school:
                raise ValidationError("Teacher/student schools must match.")
        else:
            self.fields['teacher'] = self.user

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CheckInForm, self).__init__(*args, **kwargs)
        # District admins can view teachers and students of distrct
        # School admins can view teachers and students of school
        # Teachers can view their students and cannot change the teacher field
        if user.is_district_admin and user.district is not None:
            self.fields['teacher'] = ModelChoiceField(queryset=MyUser.objects.filter(district=user.district), empty_label=None)
            self.fields['student'] = ModelChoiceField(queryset=Student.objects.filter(district=user.district), empty_label=None)
        elif user.is_school_admin and user.school is not None:
            self.fields['teacher'] = ModelChoiceField(queryset=MyUser.objects.filter(school=user.school), empty_label=None)
            self.fields['student'] = ModelChoiceField(queryset=Student.objects.filter(school=user.school), empty_label=None)
        else:
            self.fields['teacher'].widget.attrs['disabled'] = True
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


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'language', 'email', 'grade', 'district', 'school', 'teacher']

    def __init__(self, user, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        # District admins can view teachers and students of distrct
        # School admins can view teachers and students of school
        # Teachers can view their students and cannot change the teacher field
        if user.is_district_admin and user.district is not None:
            self.fields['school'] = ModelChoiceField(queryset=School.objects.filter(district=user.district), empty_label=None)
            self.fields['teacher'] = ModelChoiceField(queryset=MyUser.objects.filter(district=user.district), empty_label=None)
        elif user.is_school_admin and user.school is not None:
            self.fields['school'] = ModelChoiceField(queryset=School.objects.filter(id=user.school.id), empty_label=None)
            self.fields['teacher'] = ModelChoiceField(queryset=MyUser.objects.filter(school=user.school), empty_label=None)
        else:
            self.fields['school'] = ModelChoiceField(queryset=School.objects.filter(id=user.school.id), empty_label=None)
            self.fields['teacher'] = ModelChoiceField(queryset=MyUser.objects.filter(id=user.id), empty_label=None)

