import abc
import urllib.parse
import logging

import admin_ip_restrictor.middleware

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import resolve
from django.urls.exceptions import Resolver404

from directory_components import helpers


logger = logging.getLogger(__name__)


class RobotsIndexControlHeaderMiddlware:
    def process_response(self, request, response):
        if settings.FEATURE_FLAGS['SEARCH_ENGINE_INDEXING_OFF']:
            response['X-Robots-Tag'] = 'noindex'
        return response


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
        if settings.FEATURE_URL_PREFIX_ENABLED:
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


class IPRestrictorMiddleware(
    admin_ip_restrictor.middleware.AdminIPRestrictorMiddleware
):
    MESSAGE_UNABLE_TO_DETERMINE_IP_ADDRESS = 'Unable to determine remote IP'

    def get_ip(self, request):
        try:
            return helpers.RemoteIPAddressRetriver().get_ip_address(request)
        except LookupError:
            logger.exception(self.MESSAGE_UNABLE_TO_DETERMINE_IP_ADDRESS)
            raise Http404()

    def process_view(self, request, *args, **kwargs):
        cookie = request.COOKIES.get('ip-restrict-signature')
        if cookie and helpers.is_skip_ip_check_signature_valid(cookie):
            return None
        return super().process_view(request, *args, **kwargs)


def is_path_resolvable(path):
    if not path.endswith('/'):
        path += '/'
    try:
        resolve(path)
    except Resolver404:
        return False
    else:
        return True
