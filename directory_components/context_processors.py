from django.conf import settings


def analytics(request):
    return {
        'directory_components_analytics': {
            'GOOGLE_TAG_MANAGER_ID': settings.GOOGLE_TAG_MANAGER_ID,
            'GOOGLE_TAG_MANAGER_ENV': settings.GOOGLE_TAG_MANAGER_ENV,
            'UTM_COOKIE_DOMAIN': settings.UTM_COOKIE_DOMAIN,
        }
    }


def urls(request):
    return {
        'directory_components_urls': {
            'FEEDBACK_URL': settings.EXTERNAL_SERVICE_FEEDBACK_URL
        }
    }
