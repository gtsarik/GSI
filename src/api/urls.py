# -*- coding: utf-8 -*-
"""API urls.py"""

from django.conf.urls import include, url
from rest_framework.authtoken import views
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import (DataSetList, DataSetDetail,
                        ShapeFileList, ShapeFileDetail, ShapeFileNameDetail,
                        TimeSeriesDetail, TimeSeriesList, TimeSeriesNameDetail,
                        UploadFileAoiView, UploadFileFtpView,
                        ReportsList, ReportsDetail,
                        obtain_auth_token,
                        LogsList, LogDetail, AdditionalArguments)


urlpatterns = [
	# API
	# url(r'^step/(?P<step_id>\d+)/$', 'api.views.update_step', name='update_step'),
	# url(r'^run/(?P<run_id>\d+\.\d+\.\d+\.\d+\.\d+)/$', 'api.views.update_run',
	#	 name='update_run'),

	# execute RUNs
	url(r'^run/(?P<run_id>\w+\.\w+\.\w+\.\w+\.\w+)/$', 'api.views.update_run', name='update_run'),
	
    # Login
	url(r'^external/login/', 'api.views.external_auth_api', name='external_auth_api'),
    
    # TerraServer
	# url(r'^terraserver', 'api.views.terraserver', name='terraserver'),

    # DataSet
    url(r'^datasets-list/', DataSetList.as_view({'get': 'list'})),
    url(r'^dataset/(?P<ds_id>[0-9]+)/$', DataSetDetail.as_view()),
	# url(r'^datasets/', 'api.views.datasets_list', name='datasets_list'),
	# url(r'^polygons/', CustomerPolygonsList.as_view()),
    # url(r'^datasets/', DataSetList.as_view()), 

    # ShapeFiles
    url(r'^shapefiles-list/$', ShapeFileList.as_view({'get': 'list'})),
    url(r'^shapefile/(?P<sf_id>[0-9]+)/$', ShapeFileDetail.as_view()),
    url(r'^shapefile', ShapeFileNameDetail.as_view()),

    # TimeSeries
    url(r'^timeseries-list/$', TimeSeriesList.as_view({'get': 'list'})),
    url(r'^timeseries/(?P<shapefile_id>[0-9]+)/$', TimeSeriesDetail.as_view()),
    url(r'^timeseries', TimeSeriesNameDetail.as_view()),
    # url(r'^timeseries-list/$', TimeSeriesList.as_view()),
    # url(r'^timeseries/', TimeSeriesDetail.as_view({'get': 'list'})),

    # Reports Attribute
    # url(r'^reports-list/$', ReportsList.as_view()),
    url(r'^reports-list/$', ReportsList.as_view({'get': 'list'})),
    url(r'^reports/(?P<ds_id>[0-9]+)/$', ReportsDetail.as_view()),
   
    # upload AOI file
    url(r'^upload-aoi/(?P<ds_id>[0-9]+)/$', UploadFileAoiView.as_view()),

    # upload file to FTP
    url(r'^upload/$', UploadFileFtpView.as_view()),

    # get Logs
    url(r'^logs-list/$', LogsList.as_view({'get': 'list'})),
    url(r'^log/(?P<log_id>[0-9]+)/$', LogDetail.as_view()),
    # url(r'^shapefile', ShapeFileNameDetail.as_view()),
    
    # get Additional Arguments
    url(r'^arguments/$', AdditionalArguments.as_view()),
	
    # Auth Token
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api-token-auth/', obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
