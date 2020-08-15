from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Users
from django.db.models import Q

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'vTextField'}))
    class Meta:
        model = Users
        fields = '__all__'

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['is_staff'].initial = True


class StaffUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'vTextField'}))
    class Meta:
        model = Users
        fields = '__all__'

    def save(self, commit=True):
        user = super(StaffUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\"../password/\">this form</a>.")
    )

    class Meta:
        model = Users
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'address',)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['username'].widget.attrs['class'] = 'vTextField'
        self.fields['first_name'].widget.attrs['class'] = 'vTextField'
        self.fields['last_name'].widget.attrs['class'] = 'vTextField'
        self.fields['email'].widget.attrs['class'] = 'vTextField'
        self.fields['address'].widget.attrs['class'] = 'vLargeTextField'


class AdminUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\"../password/\">this form</a>.")
    )

    class Meta:
        model = Users
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'address','is_staff', 'is_active',)
        

    def clean_password(self):
        return self.initial["password"]

    def __init__(self, *args, **kwargs):
        super(AdminUserChangeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['username'].widget.attrs['class'] = 'vTextField'
        self.fields['first_name'].widget.attrs['class'] = 'vTextField'
        self.fields['last_name'].widget.attrs['class'] = 'vTextField'
        self.fields['email'].widget.attrs['class'] = 'vTextField'
        self.fields['address'].widget.attrs['class'] = 'vLargeTextField'


class StaffUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\"../password/\">this form</a>.")
    )

    class Meta:
        model = Users
        fields = '__all__'
        

    def clean_password(self):
        return self.initial["password"]
