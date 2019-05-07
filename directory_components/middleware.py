import abc
import logging
import urllib.parse

from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation
from django.urls import resolve
from django.urls.exceptions import Resolver404
from django.middleware.locale import LocaleMiddleware

from directory_components import constants
from directory_components import helpers

logger = logging.getLogger(__name__)


class MaintenanceModeMiddleware:
    maintenance_url = 'https://sorry.great.gov.uk'

    def process_request(self, request):
        if settings.FEATURE_FLAGS['MAINTENANCE_MODE_ON']:
            return redirect(self.maintenance_url)


class NoCacheMiddlware:
    """Tell the browser to not cache the pages.

    Information that should be kept private can be viewed by anyone
    with access to the files in the browser's cache directory.

    """

    def process_response(self, request, response):
        if getattr(request, 'sso_user', None):
            response['Cache-Control'] = 'no-store, no-cache'
        return response


class AbstractPrefixUrlMiddleware(abc.ABC):

    @property
    @abc.abstractmethod
    def prefix(self):
        return ''

    def process_request(self, request):
        redirect_url = self.get_redirect_url(request)
        if redirect_url:
            return redirect(redirect_url)

    def get_redirect_url(self, request):
        prefixer = helpers.UrlPrefixer(request=request, prefix=self.prefix)
        path = None
        host = self.get_redirect_domain(request)
        if not prefixer.is_path_prefixed and is_path_resolvable(prefixer.path):
            path = prefixer.full_path
        if host and not path and is_path_resolvable(request.path):
            path = request.get_full_path(force_append_slash=True)
        if host and path:
            return urllib.parse.urljoin(host, path)
        elif path:
            return path

    @staticmethod
    def get_redirect_domain(request):
        if settings.URL_PREFIX_DOMAIN:
            if not request.get_raw_uri().startswith(
                    settings.URL_PREFIX_DOMAIN
            ):
                return settings.URL_PREFIX_DOMAIN


def is_path_resolvable(path):
    if not path.endswith('/'):
        path += '/'
    try:
        resolve(path)
    except Resolver404:
        return False
    else:
        return True


class CountryMiddleware:
    def process_request(self, request):
        country_code = helpers.get_country_from_querystring(request)
        if country_code:
            request.COUNTRY_CODE = country_code

    def process_response(self, request, response):
        """
        Shares config with the language cookie as they serve a similar purpose
        """

        if hasattr(request, 'COUNTRY_CODE'):
            response.set_cookie(
                key=constants.COUNTRY_COOKIE_NAME,
                value=request.COUNTRY_CODE,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN
            )
        return response


class LocaleQuerystringMiddleware(LocaleMiddleware):
    def process_request(self, request):
        super().process_request(request)
        language_code = helpers.get_language_from_querystring(request)
        if language_code:
            translation.activate(language_code)
            request.LANGUAGE_CODE = translation.get_language()


class PersistLocaleMiddleware:
    def process_response(self, request, response):
        if hasattr(settings, 'LANGUAGE_COOKIE_DEPRECATED_NAME'):
            response.delete_cookie(
                key=settings.LANGUAGE_COOKIE_DEPRECATED_NAME
            )
        response.set_cookie(
            key=settings.LANGUAGE_COOKIE_NAME,
            value=translation.get_language(),
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN
        )
        return response


class ForceDefaultLocale:
    """
    Force translation to English before view is called, then putting the user's
    original language back after the view has been called, laying the ground
    work for`EnableTranslationsMixin` to turn on the desired locale. This
    provides per-view translations.
    """

    def process_request(self, request):
        translation.activate(settings.LANGUAGE_CODE)

    def process_response(self, request, response):
        if hasattr(request, 'LANGUAGE_CODE') and request.LANGUAGE_CODE:
            translation.activate(request.LANGUAGE_CODE)
        return response

    def process_exception(self, request, exception):
        if hasattr(request, 'LANGUAGE_CODE') and request.LANGUAGE_CODE:
            translation.activate(request.LANGUAGE_CODE)
