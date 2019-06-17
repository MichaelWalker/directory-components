from django.conf.urls import url

from demo import views

urlpatterns = [
    url(
        r'^$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/index.html'},
        name='index',
    ),
    url(
        r'^404/$',
        views.Trigger404View.as_view(),
        name='404',
    ),
    url(
        r'^500/$',
        views.Trigger500ErrorView.as_view(),
        name='500',
    ),
    url(
        r'^great-domestic-header-footer/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/great-domestic-header-footer.html'},
        name='great-domestic-header-footer',
    ),
    url(
        r'^elements/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/elements.html'},
        name='elements',
    ),
    url(
        r'^widgets/$',
        views.DemoFormView.as_view(),
        name='widgets',
    ),
    url(
        r'^form-errors/$',
        views.DemoFormErrorsView.as_view(),
        name='form-errors',
    ),
    url(
        r'^components/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/components.html'},
        name='components',
    ),
    url(
        r'^buttons/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/buttons.html'},
        name='buttons',
    ),
    url(
        r'^full-width-banners/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/full-width-banners.html'},
        name='full-width-banners',
    ),
    url(
        r'^banners/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/banners.html'},
        name='banners',
    ),
    url(
        r'^message-boxes/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/message-boxes.html'},
        name='message-boxes',
    ),
    url(
        r'^cards/$',
        views.DemoCardsView.as_view(),
        {'template_name': 'demo/cards.html'},
        name='cards',
    ),
    url(
        r'^breadcrumbs/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/breadcrumbs.html'},
        name='breadcrumbs',
    ),
    url(
        r'^responsive/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/responsive.html'},
        name='responsive',
    ),
    url(
        r'^template-tags/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/cms.html'},
        name='cms-tags',
    ),
    url(
        r'^great-international-header-footer/$',
        views.InternationalHeaderView.as_view(),
        {'template_name': 'demo/great-international-header-footer.html'},
        name='great-international-header-footer',
    ),
    url(
        r'^invest-header/$',
        views.InvestHeaderView.as_view(),
        {'template_name': 'demo/invest-header.html'},
        name='invest-header',
    ),
]

handler404 = 'directory_components.views.handler404'

handler500 = 'directory_components.views.handler500'
