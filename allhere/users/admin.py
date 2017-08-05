from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import UserAH


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserAH


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This email has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = UserAH

    def clean_username(self):
        email = self.cleaned_data["email"]
        try:
            UserAH.objects.get(email=email)
        except UserAH.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_username'])

@admin.register(UserAH)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = AuthUserAdmin.fieldsets + (
            ('User Profile', {'fields': ('email',
                                        'school'
                                        )}),
    )
    list_display = ('email', 'name','school')
    search_fields = ['name', 'email']
    filter_horizontal = ('teams', )
    list_filter = ('email', 'school') 

admin.site.register(Student, admin.ModelAdmin)

admin.site.register(Group, admin.ModelAdmin)
admin.site.register(School, admin.ModelAdmin)
admin.site.register(Team, admin.ModelAdmin)

admin.site.register(Attendance, admin.ModelAdmin)
admin.site.register(CheckIns, admin.ModelAdmin)
admin.site.register(CheckInsFormText, admin.ModelAdmin)