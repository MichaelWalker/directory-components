from bs4 import BeautifulSoup
from directory_constants import urls
import pytest

from django.template.loader import render_to_string

from directory_components import context_processors


@pytest.mark.parametrize('template_name', [
    'directory_components/header_footer/international_header.html',
    'directory_components/header_footer/international_footer.html',
    'directory_components/header_footer/domestic_header.html',
    'directory_components/header_footer/domestic_footer.html',
    'directory_components/header_footer/domestic_header_static.html',
])
def test_templates_rendered(template_name):
    html = render_to_string(template_name)
    assert '<div' in html
    assert '<ul' in html
    assert '<a' in html


@pytest.mark.parametrize('template_name', (
    'directory_components/header_footer/domestic_header.html',
    )
)
def test_header_logged_in(template_name):
    context = {
        'sso_is_logged_in': True,
        'sso_login_url': 'login.com',
        'sso_logout_url': 'logout.com',
        **context_processors.header_footer_processor(None),
    }
    html = render_to_string(template_name, context)
    assert 'Sign in' not in html
    assert context['sso_login_url'] not in html
    assert 'Sign out' in html
    assert context['sso_logout_url'] in html


@pytest.mark.parametrize('template_name', (
    'directory_components/header_footer/domestic_header.html',
    )
)
def test_header_logged_out(template_name):
    context = {
        'sso_is_logged_in': False,
        'sso_login_url': 'login.com',
        'sso_logout_url': 'logout.com',
        **context_processors.header_footer_processor(None),
    }
    html = render_to_string(template_name, context)
    assert 'Sign in' in html
    assert context['sso_login_url'] in html
    assert 'Sign out' not in html
    assert context['sso_logout_url'] not in html


def test_header_domestic_news_section_off(settings):
    context = {
        'features': {'NEWS_SECTION_ON': False},
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None)
    }
    template_name = 'directory_components/header_footer/domestic_header.html'
    html = render_to_string(template_name, context)
    assert urls.GREAT_DOMESTIC_NEWS not in html


def test_header_international_news_section_off(settings):
    context = {
        'features': {'NEWS_SECTION_ON': False},
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None)
    }
    template_name = 'directory_components/header_footer/domestic_header.html'
    html = render_to_string(template_name, context)
    assert urls.GREAT_INTERNATIONAL_NEWS not in html


@pytest.mark.parametrize('url', [
    urls.SERVICES_GREAT_DOMESTIC,
    urls.GREAT_INTERNATIONAL,
    urls.ADVICE,
    urls.MARKETS,
    urls.GREAT_DOMESTIC_NEWS,
])
def test_urls_exist_in_domestic_header(url, settings):
    context = {
        'features': {'NEWS_SECTION_ON': True},
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None)
    }
    template_name = (
        'directory_components/header_footer/domestic_header.html')
    assert url in render_to_string(template_name, context)


@pytest.mark.parametrize('url', [
    urls.SERVICES_GREAT_DOMESTIC,
    urls.GREAT_INTERNATIONAL,
    urls.SERVICES_INVEST,
    urls.SERVICES_FAS,
    urls.GREAT_INTERNATIONAL_INDUSTRIES,
    urls.GREAT_INTERNATIONAL_HOW_TO_DO_BUSINESS_WITH_THE_UK,
    urls.GREAT_INTERNATIONAL_NEWS,
])
def test_urls_exist_in_international_header(url, settings):
    context = {
        'features': {
            'NEWS_SECTION_ON': True,
            'HOW_TO_DO_BUSINESS_ON': True,
        },
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None)
    }
    template_name = (
        'directory_components/header_footer/international_header.html')
    assert url in render_to_string(template_name, context)


@pytest.mark.parametrize('url', [
    urls.GREAT_INTERNATIONAL,
    urls.CONTACT_US,
    urls.PRIVACY_AND_COOKIES,
    urls.TERMS_AND_CONDITIONS,
    urls.PERFORMANCE_DASHBOARD,
    urls.DIT,
])
def test_urls_exist_in_domestic_footer(url, settings):
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    template_name = (
        'directory_components/header_footer/domestic_footer.html')
    assert url in render_to_string(template_name, context)


@pytest.mark.parametrize('url', [
    urls.SERVICES_GREAT_DOMESTIC,
    urls.CONTACT_US,
    urls.PRIVACY_AND_COOKIES,
    urls.TERMS_AND_CONDITIONS,
    urls.DIT,
])
def test_urls_exist_in_international_footer_v2(url, settings):
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    template_name = (
        'directory_components/header_footer/international_footer.html')
    assert url in render_to_string(template_name, context)


@pytest.mark.parametrize('title,element_id,url', (
    (
        'Advice',
        'header-advice',
        urls.ADVICE,
    ),
    (
        'Markets',
        'header-markets',
        urls.MARKETS,
    ),
    (
        'News and events',
        'header-news',
        urls.GREAT_DOMESTIC_NEWS,
    ),
))
def test_domestic_header_ids_match_urls_and_text(
    title, element_id, url, settings
):
    context = {
        'features': {
            'NEWS_SECTION_ON': True
        },
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
    }

    html = render_to_string(
        'directory_components/header_footer/domestic_header.html', context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)

    assert element.attrs['href'] == url
    if title:
        assert element.string == title


@pytest.mark.parametrize('title,element_id,url', (
    (
        'Invest',
        'header-invest',
        urls.SERVICES_INVEST,
    ),
    (
        'Find a UK supplier',
        'header-fas',
        urls.SERVICES_FAS,
    ),
    (
        'Industries',
        'header-industries',
        urls.GREAT_INTERNATIONAL_INDUSTRIES,
    ),
    (
        'How to do business with the UK',
        'header-how-to-do-business-with-the-uk',
        urls.GREAT_INTERNATIONAL_HOW_TO_DO_BUSINESS_WITH_THE_UK,
    ),
    (
        'News',
        'header-news',
        urls.GREAT_INTERNATIONAL_NEWS,
    ),
    (
        '',
        'great-header-logo',
        urls.SERVICES_GREAT_INTERNATIONAL,
    ),
))
def test_international_header_ids_match_urls_and_text(
    title, element_id, url, settings
):
    context = {
        'features': {
            'NEWS_SECTION_ON': True,
            'HOW_TO_DO_BUSINESS_ON': True
        },
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
    }

    html = render_to_string(
        'directory_components/header_footer/international_header.html',
        context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)

    assert element.attrs['href'] == url
    if title:
        assert element.string == title


@pytest.mark.parametrize('title,element_id,url', (
    (
        'Contact us',
        'footer-contact',
        urls.CONTACT_US,
    ),
    (
        'Privacy and cookies',
        'footer-privacy-and-cookies',
        urls.PRIVACY_AND_COOKIES,
    ),
    (
        'Terms and conditions',
        'footer-terms-and-conditions',
        urls.TERMS_AND_CONDITIONS,
    ),
    (
        'Performance',
        'footer-performance',
        urls.PERFORMANCE_DASHBOARD,
    ),
    (
        'Department for International Trade on GOV.UK',
        'footer-dit',
        urls.DIT
    ),
    (
        'Go to the page for international businesses',
        'footer-international',
        urls.GREAT_INTERNATIONAL
    ),
))
def test_domestic_footer_ids_match_urls_and_text(
    title, element_id, url, settings
):
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    html = render_to_string(
        'directory_components/header_footer/domestic_footer.html', context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)
    assert element.attrs['href'] == url
    if title:
        assert element.string == title


@pytest.mark.parametrize('title,element_id,url', (
    (
        'Contact us',
        'footer-contact',
        urls.CONTACT_US,
    ),
    (
        'Privacy and cookies',
        'footer-privacy-and-cookies',
        urls.PRIVACY_AND_COOKIES,
    ),
    (
        'Terms and conditions',
        'footer-terms-and-conditions',
        urls.TERMS_AND_CONDITIONS,
    ),
    (
        'Department for International Trade on GOV.UK',
        'footer-dit',
        urls.DIT
    ),
    (
        'Go to the page for UK businesses',
        'footer-domestic',
        urls.SERVICES_GREAT_DOMESTIC
    ),
))
def test_international_footer_ids_match_urls_and_text(
    title, element_id, url, settings
):
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    html = render_to_string(
        'directory_components/header_footer/international_footer.html',
        context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)
    assert element.attrs['href'] == url
    if title:
        assert element.string == title
