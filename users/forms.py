from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, City


def forbidden_users(value):
    check_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root', 'email', 'user',
                   'join', 'sql', 'static', 'python', 'delete', 'sex', 'sexy']
    if value.lower() in check_users:
        raise ValidationError('Invalid name for user, this is a reserverd word.')


def invalid_user(value):
    if '@' in value or '+' in value or '-' in value or ':' in value:
        raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , +, :')


def unique_email(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this email already exists.')


def unique_user(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this username already exists.')


class SignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={}), max_length=30, required=True, )
    email = forms.CharField(widget=forms.EmailInput(attrs={}), max_length=100, required=True, )
    password = forms.CharField(widget=forms.PasswordInput(attrs={}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={}), required=True,
                                       label="Confirm your password.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(forbidden_users)
        self.fields['username'].validators.append(invalid_user)
        self.fields['username'].validators.append(unique_user)
        self.fields['email'].validators.append(unique_email)

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your Username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password'}), required=True)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'country', 'city', 'address',
                  'phone_number', 'profile_picture', 'interest', 'about_me']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter Your First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter Your Last Name'}),
            'date_of_birth': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter Your Address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Your Phone Number'}),
            'interest': forms.TextInput(attrs={'placeholder': 'What Topic(s) attract(s) You?'}),
            'about_me': forms.Textarea(attrs={'placeholder': 'Few Things About You...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
