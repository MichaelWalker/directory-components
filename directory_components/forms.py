from django import forms
from django.forms import Select
from django.db.models.fields import BLANK_CHOICE_DASH

from directory_components import fields as components_fields
from directory_constants.constants.choices import COUNTRY_CHOICES

from directory_components import helpers

COUNTRIES = BLANK_CHOICE_DASH + COUNTRY_CHOICES


class DirectoryComponentsFormMixin:

    use_required_attribute = False
    error_css_class = 'form-group-error'

    def as_p(self):
        return self._html_output(
            normal_row=(
                '<p%(html_class_attr)s>%(label)s %(help_text)s %(field)s</p>'
            ),
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="form-hint">%s</span>',
            errors_on_separate_row=True
        )


class Form(DirectoryComponentsFormMixin, forms.Form):
    pass


class CountryForm(Form):
    country = components_fields.ChoiceField(
        label='Country',
        widget=Select(attrs={'id': 'js-country-select'}),
        choices=COUNTRIES
    )


def get_country_form_initial_data(request):
    return {
        'country': helpers.get_user_country(request).upper() or None
    }
