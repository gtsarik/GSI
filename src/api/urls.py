# -*- coding: utf-8 -*-
"""API urls.py"""

from django.conf.urls import include, url
from rest_framework.authtoken import views
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import CustomerPolygonsList


urlpatterns = [
	# API
	# url(r'^step/(?P<step_id>\d+)/$', 'api.views.update_step', name='update_step'),
	# url(r'^run/(?P<run_id>\d+\.\d+\.\d+\.\d+\.\d+)/$', 'api.views.update_run',
	#	 name='update_run'),

	# api for the execute runs
	url(r'^run/(?P<run_id>\w+\.\w+\.\w+\.\w+\.\w+)/$', 'api.views.update_run', name='update_run'),
	# api for the gsi
	
	url(r'^external/login/', 'api.views.external_auth_api', name='external_auth_api'),
	url(r'^terraserver', 'api.views.terraserver', name='terraserver'),
	# url(r'^datasets/', 'api.views.datasets_list', name='datasets_list'),
	url(r'^polygons/$', CustomerPolygonsList.as_view()),
	
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api-token-auth/', views.obtain_auth_token),
	
	url(r'^dataset/(?P<ds_id>\w+)/$', 'api.views.dataset', name='dataset'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
