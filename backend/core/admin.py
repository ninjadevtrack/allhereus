from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import F
from core.models import MyUser, Student, CheckIn, District, School, Section, SectionStudent, SectionTeacher
import csv
from django.http import HttpResponse
from datetime import datetime
from .utils import download_checkins_csv
# https://github.com/django/django/blob/a96b981d84367fd41b1df40adf3ac9ca71a741dd/django/contrib/auth/forms.py#L64-L150
class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # https://stackoverflow.com/a/15630360/3555105
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\'../password/\'>this form</a>."))

    class Meta:
        model = MyUser
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


# https://github.com/django/django/blob/8346680e1ca4a8ddc8190baf3f5f944f6418d5cf/django/contrib/auth/admin.py#L42-L207
class UserAdmin(BaseUserAdmin):
    # https://stackoverflow.com/a/40715745/3555105
    def image_tag(self, obj):
        return format_html(f'<img src="{obj.avatar_url}" />')
    image_tag.short_description = 'User Avatar'

    readonly_fields = ('last_updated', 'date_joined', 'image_tag')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'image_tag')}),
        ('Personal Info', {'fields': ('first_name', 'last_name',)}),
        ('Account Info', {'fields': ('role', 'is_manager',)}),
        ('Organization Info', {'fields': ('district', 'school',)}),
        # ('Organization Info', {'fields': ('district', 'school', 'team',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'last_updated', 'date_joined')}),
        ('Soft deletes', {'fields': ('is_deleted', 'deleted_on')})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('district','school','last_name','first_name','email', 'role', 'is_staff', 'is_deleted')
    list_filter = ('is_superuser', 'role', 'is_staff', 'is_active', 'groups')
    search_fields = ('email','district__name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

class StudentAdmin(admin.ModelAdmin):
    model = Student

    fieldsets = (
        ('Personal Info',
            {'fields':
                ('student_id','is_active','first_name', 'last_name',
                'language','email','grade','total_absences')}),
        ('Organization Info', {'fields': ('district', 'school','teacher')}),
        ('Guardians Info', {'fields':
            ('parent_first_name', 'parent_last_name','phone','parent_email')}),
        ('Soft deletes', {'fields': ('is_deleted', 'deleted_on')})
    )

    list_display = ('district','school','teacher','last_name','first_name','email', 'is_active','is_deleted')
    list_filter = ('is_active', 'is_deleted')
    search_fields = ('last_name','first_name','district__name','school__name')
    ordering = ('district__name','school__name','last_name','first_name')

class DisctrictAdmin(admin.ModelAdmin):
    list_display = ('name','is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name',)
    ordering = ('name',)

    class Meta:
        model = District
        fields = '__all__'


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('district','name','is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('district__name','name')
    ordering = ('district__name','name')

    class Meta:
        model = School
        fields = '__all__'

class SectionStudentInline(admin.TabularInline):
    model = SectionStudent

    # Since these are all ednudge-manageed, disable the ability to add/delete
    def has_add_permission(self, request, obj=None):
        return False
    can_delete = False

    def get_extra(self, request, obj=None, **kwargs):
        if obj.ednudge_is_enabled:
            return 0
        else:
            return 1

    fields = ['student','ednudge_enrollment_id','is_deleted']
    readonly_fields = ['student','ednudge_is_enabled','ednudge_person_id','ednudge_enrollment_id','ednudge_section_id',]
    ordering = ('student__last_name','student__first_name',)

class SectionTeacherInline(admin.TabularInline):
    model = SectionTeacher

    # Since these are all ednudge-manageed, disable the ability to add/delete
    def has_add_permission(self, request, obj=None):
        return False
    can_delete = False

    def get_extra(self, request, obj=None, **kwargs):
        if obj.ednudge_is_enabled:
            return 0
        else:
            return 1

    fields = ['teacher','ednudge_enrollment_id','is_deleted']
    readonly_fields = ['teacher','ednudge_is_enabled','ednudge_person_id','ednudge_enrollment_id','ednudge_section_id',]
    ordering = ('teacher__last_name','teacher__first_name',)


class SectionAdmin(admin.ModelAdmin):
    class Meta:
        model = Section

    inlines = [
        SectionTeacherInline,
        SectionStudentInline,
    ]

    list_display = ('district', 'school', 'ednudge_section_local_id','name', 'is_deleted',)
    list_filter = ('is_deleted',)
    search_fields = ('district__name','school__name', 'name')
    ordering = ('district__name','school__name','name')

    fieldsets = (
        ('Section Info', {
            'fields': (
                'name','subject','period',
                'term_name','term_start_date', 'term_end_date',
                )}),
        ('Organization Info', {'fields': ('district', 'school',)}),
        ('Soft deletes', {
            'classes': ('collapse',),
            'fields': ('is_deleted', 'deleted_on')}),
        ('Ednudge Integration', {
            'classes': ('collapse',),
            'fields': (
                'ednudge_is_enabled', 'ednudge_section_id',
                'ednudge_section_local_id', 'ednudge_merkleroot')}),
    )

    readonly_fields = ['ednudge_is_enabled','ednudge_section_id', 'ednudge_section_local_id', 'ednudge_merkleroot']


class CheckInAdmin(admin.ModelAdmin):
    ordering = ('teacher', 'student', 'date',)
    list_display = ('district', 'school', 'teacher','student', 'date', 'status')
    search_fields = ('student__district__name', 'student__school__name', 'teacher__first_name', 'teacher__last_name', 'student__first_name', 'student__last_name', 'date')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('student').annotate(
            _district=F('student__district'),
            _school=F('student__school')
        )
        return queryset

    def district(self, obj):
        return obj.student.district
    
    def school(self, obj):
        return obj.student.school

    def download_csv(self, request, queryset):
        return download_checkins_csv(queryset)
    download_csv.short_description = "Download CSV"

    district.admin_order_field = '_district'
    school.admin_order_field = '_school'
    actions = [download_csv]


admin.site.register(MyUser, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(CheckIn, CheckInAdmin)
admin.site.register(District, DisctrictAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Section, SectionAdmin)
