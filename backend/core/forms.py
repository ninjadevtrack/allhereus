from django.forms import ModelForm, ModelChoiceField, IntegerField, NumberInput, TypedChoiceField, ValidationError, CharField
from .models import MyUser, CheckIn, Student, School, Strategy



class CheckInForm(ModelForm):
    """Custom class to create/edit CheckIn"""

    success_score = IntegerField(widget=NumberInput(attrs={'type': 'range', 'step': '1', 'min': '0', 'max': '10'}))

    class Meta:
        model = CheckIn
        fields = ['date', 'teacher', 'student', 'status',
                  'mode', 'notify_school_admin', 'success_score',
                  'info_learned', 'info_better',]

    def save(self, *args, **kwargs):
        if self.instance.id == None:
            self.instance.strategy = self.cleaned_data['strategy']
        return super().save(*args, **kwargs)


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

    def __init__(self, user, student, strategy, *args, **kwargs):
        self.user = user
        super(CheckInForm, self).__init__(*args, **kwargs)
        if self.instance.id == None:
            self.fields['strategy'] = ModelChoiceField(
                queryset=Strategy.objects.for_district(user.district).as_of(),
                required=False)
        if strategy != None:
            self.fields['strategy'].initial=strategy

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
            #self.fields['student'] = ModelChoiceField(queryset=Student.objects.filter(teacher=user), empty_label=None)
            self.fields['student'] = ModelChoiceField(queryset=user.students, empty_label=None)

        if student is not None:
            self.fields['student'] = ModelChoiceField(queryset=Student.objects.filter(pk=student.id), empty_label=None)

        self.fields['success_score'] = TypedChoiceField([(x, x) for x in range(0, 11)])
        self.fields['info_learned'].widget.attrs['rows'] = 2
        self.fields['info_better'].widget.attrs['rows'] = 2

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        # remove the empty states for TypedChoiceField which is used by status
        # and mode.
        # see: https://stackoverflow.com/a/29429615/3720597
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, TypedChoiceField):
                field.choices = [('', "Select one")] + field.choices[1:]

class ProfileForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'school', 'department', 'first_name', 'last_name', 'subject', 'grade']
        exclude = ['district']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        # District admins can view all schools in the district
        # School admins can view only their school
        # Teachers can view only their school
        if user.is_district_admin and user.district is not None:
            self.fields['school'] = ModelChoiceField(queryset=School.objects.filter(district=user.district), empty_label=None)
        elif user.is_school_admin and user.school is not None:
            self.fields['school'] = ModelChoiceField(queryset=School.objects.filter(id=user.school.id), empty_label=None)
        elif user.school is not None:
            self.fields['school'] = ModelChoiceField(queryset=School.objects.filter(id=user.school.id), empty_label=None)
        else:
            self.fields['school'] = ModelChoiceField(queryset=School.objects.none(), empty_label=None)


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id',
            'first_name',
            'last_name',
            'language',
            'email',
            'grade',
            'district',
            'school',
            'teacher',
            'parent_first_name',
            'parent_last_name',
            'phone',
            'parent_email',
        ]

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
        elif user.school is not None:
            self.fields['school'] = ModelChoiceField(queryset=School.objects.filter(id=user.school.id), empty_label=None)
            self.fields['teacher'] = ModelChoiceField(queryset=MyUser.objects.filter(id=user.id), empty_label=None)
        else:
            self.fields['school'] = ModelChoiceField(queryset=School.objects.none(), empty_label=None)
            self.fields['teacher'] = ModelChoiceField(queryset=MyUser.objects.filter(id=user.id), empty_label=None)
