import datetime

from django import forms
from django.forms import widgets
from django.forms.extras import widgets as extras_widgets
from django.utils import encoding, safestring
from django.utils.translation import ugettext_lazy as _

from piplmesh.account import fields, form_fields, models

class RadioFieldRenderer(widgets.RadioFieldRenderer):
    """
    RadioSelect renderer which adds ``first`` and ``last`` style classes
    to first and last radio widgets.
    """

    def _render_widgets(self):
        for i, w in enumerate(self):
            classes = []
            if i == 0:
                classes.append('first')
            if i == len(self.choices) - 1:
                classes.append('last')

            cls = ''
            if classes:
                cls = u' class="%s"' % (u' '.join(classes),)

            yield u'<li%s>%s</li>' % (cls, encoding.force_unicode(w))

    def render(self):
        return safestring.mark_safe(u'<ul>\n%s\n</ul>' % (u'\n'.join(self._render_widgets())),)

class UserUsernameForm(forms.Form):
    """
    Class with username form
    """

    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages = {
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})

    def clean_username(self):
        # This method checks whether the username exists in case-insensitive manner
        username = self.cleaned_data['username']
        if models.User.objects(username__iexact=username).count():
            raise forms.ValidationError(_("A user with that username already exists."))
        return username

class UserPasswordForm(forms.Form):
    """
    Class with user password form
    """

    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))

    def clean_password2(self):
        # This method checks whether the passwords match
        if self.cleaned_data.has_key('password1') and self.cleaned_data['password1'] == self.cleaned_data['password2']:
            return self.cleaned_data['password2']
        raise forms.ValidationError(_("Passwords do not match."))

class UserNewPasswordForm(forms.Form):
    """
    Class with user new password form
    """
    # TODO: Try to inherit UserPasswordForm and just override the settings ? Is that possible ?
    password1 = forms.CharField(label=_("New Password"),
        widget=forms.PasswordInput,
        required=False)
    password2 = forms.CharField(label=_("New Password confirmation"),
        widget=forms.PasswordInput,
        required=False,
        help_text = _("Enter the same password as above, for verification."))

    def clean_password2(self):
        # This method checks whether the passwords match
        if self.cleaned_data.has_key('password1') and self.cleaned_data['password1'] == self.cleaned_data['password2']:
            return self.cleaned_data['password2']
        raise forms.ValidationError(_("Passwords do not match."))

class UserBasicInfoForm(forms.Form):
    """
    Class with user basic information form
    """

    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))
    email = forms.EmailField(label=_("E-mail"))
    gender = forms.ChoiceField(
        label=_("Gender"),
        required=False,
        choices=fields.GENDER_CHOICES,
        widget=forms.RadioSelect(renderer=RadioFieldRenderer),
    )
    birthdate = form_fields.LimitedDateTimeField(
        upper_limit=datetime.datetime.today(),
        lower_limit=datetime.datetime.today() - datetime.timedelta(models.LOWER_DATE_LIMIT),
        label=_("Birth date"),
        required=False,
        widget=extras_widgets.SelectDateWidget(
            years=[
            y for y in range(
                datetime.datetime.today().year,
                (datetime.datetime.today() - datetime.timedelta(models.LOWER_DATE_LIMIT)).year,
                -1,
            )
            ],
        ),
    )

class UserAdditionalInfoForm(forms.Form):
    """
    Class with user additional information form
    """

    profile_image = forms.CharField(label=_("Profile image"),required=False)

class UserRegistrationForm(UserUsernameForm,UserPasswordForm,UserBasicInfoForm):
    """
    Class with Registration form
    """

class AccountForm(UserBasicInfoForm,UserAdditionalInfoForm,UserNewPasswordForm):
    """
    Class with account form
    """

    old_password = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput,
        help_text = _("Enter your current password, for verification."))