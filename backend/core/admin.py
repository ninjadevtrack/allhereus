from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from core.models import MyUser, Student, CheckIn, District, School


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
        ('Important dates', {'fields': ('last_login', 'last_updated', 'date_joined')})
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
    list_display = ('email', 'is_staff', 'district')
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


class SchoolInline(admin.StackedInline):
    model = School
    extra = 1


class StudentInline(admin.StackedInline):
    model = Student
    extra = 1


class DisctrictAdmin(admin.ModelAdmin):
    inlines = [
        SchoolInline,
        StudentInline,
    ]

    class Meta:
        model = District
        fields = '__all__'


class SchoolAdmin(admin.ModelAdmin):

    class Meta:
        model = School
        fields = '__all__'


admin.site.register(MyUser, UserAdmin)
admin.site.register(Student)
admin.site.register(CheckIn)
admin.site.register(District, DisctrictAdmin)
admin.site.register(School, SchoolAdmin)
