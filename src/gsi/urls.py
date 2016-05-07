from django.conf.urls.static import static
from django.conf import settings

"""GSI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required

from gsi.views import UploadStaticDataView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # temporary blocking
    url(r'^$', 'gsi.views.blocking', name='block'),


    # index
    url(r'^index/$', 'gsi.views.index', name='index'),


    # upload file
    # url(r'^upload-file/$', UploadStaticDataView.as_view(), name='upload_file'),
    url(r'^upload-file/$', 'gsi.views.upload_file', name='upload_file'),


    # run base
    url(r'^run/setup/$', 'gsi.views.run_setup', name='run_setup'),
    url(r'^run/new/$', 'gsi.views.new_run', name='new_run'),
    url(r'^run/(?P<run_id>\d+)/$', 'gsi.views.run_update',
        name='run_update'),

    # run base view results
    url(r'^run/(?P<run_id>\d+)/view-results/$', 'gsi.views.view_results', name='view_results'),

    # run base view folder results
    url(r'^run/(?P<run_id>\d+)/view-results/(?P<prev_dir>[%\w]+)/(?P<dir>\w+)/$', 'gsi.views.view_results_folder', name='view_results_folder'),

    # submit a run
    url(r'^run/submit/$', 'gsi.views.submit_run', name='submit_run'),

    # execute run
    url(r'^run/execute/(?P<run_id>\w+)/$', 'gsi.views.execute_runs', name='execute_runs'),

    # run progress
    url(r'^run/progress/$', 'gsi.views.run_progress', name='run_progress'),

    # run details
    url(r'^run/details/(?P<run_id>\d+)/$', 'gsi.views.run_details', name='run_details'),

    # log view cards
    url(r'^run/(?P<run_id>\d+)/card/log/(?P<card_id>\d+)/$', 'gsi.views.view_log_file', name='view_log_file'),

    # setup static data
    url(r'^run/static-data/setup/$', 'gsi.views.static_data_setup', name='static_data_setup'),

    # setup home variable
    url(r'^run/home-variable/setup/$', 'gsi.views.home_variable_setup', name='home_variable_setup'),

    # audit history
    url(r'^run/(?P<run_id>\d+)/audit-history/$', 'gsi.views.audit_history', name='audit_history'),

    # environment groups
    url(r'^run/environment-groups/$', 'gsi.views.environment_groups', name='environment_groups'),

    # environment groups edit
    url(r'^run/environment-group/add/$', 'gsi.views.environment_group_add',
        name='environment_group_add'),
    url(r'^run/environment-group/(?P<env_id>\d+)/$', 'gsi.views.environment_group_edit',
        name='environment_group_edit'),

    # areas
    url(r'^run/areas/list/$', 'gsi.views.areas', name='areas'),

    # areas edit
    url(r'^run/area/add/$', 'gsi.views.area_add', name='area_add'),
    url(r'^run/area/(?P<area_id>\d+)/$', 'gsi.views.area_edit', name='area_edit'),

    # years group
    url(r'^run/years-group/list/$', 'gsi.views.years_group', name='years_group'),

    # years group edit
    url(r'^run/years-group/add/$', 'gsi.views.years_group_add', name='years_group_add'),
    url(r'^run/years-group/(?P<yg_id>\d+)/$', 'gsi.views.years_group_edit', name='years_group_edit'),

    # satellite
    url(r'^run/satellite/list/$', 'gsi.views.satellite', name='satellite'),

    # satellite edit
    url(r'^run/satellite/add/$', 'gsi.views.satellite_add', name='satellite_add'),
    url(r'^run/satellite/(?P<satellite_id>\d+)/$', 'gsi.views.satellite_edit', name='satellite_edit'),


    # card sequence for new run base
    url(r'^run/card-sequence/add/$', 'gsi.views.run_new_card_sequence_add',
        name='run_new_card_sequence_add'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/$', 'gsi.views.run_new_card_sequence_update',
        name='run_new_card_sequence_update'),
    url(r'^run/card-sequence/list/$', 'gsi.views.run_new_card_sequence_list',
        name='run_new_card_sequence_list'),

    url(r'^run/(?P<run_id>\d+)/card-sequence/add/$', 'gsi.views.add_card_sequence',
        name='add_card_sequence'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/$', 'gsi.views.card_sequence_update',
        name='card_sequence_update'),

    url(r'^run/(?P<run_id>\d+)/card-sequence/setup/$', 'gsi.views.card_sequence',
        name='card_sequence'),

    # -------------------------------------------------------------------- ???

    # card item edit for card sequence // runID->csID->card_item
    # url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/card-item/(?P<card_item_id>\d+)/$',
    #     'gsi.views.card_item_update', name='card_item_update'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/qrf/(?P<qrf_id>\d+)/$',
        'gsi.views_cs_card_runid_csid.cs_runid_csid_qrf_edit', name='cs_runid_csid_qrf_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/rfscore/(?P<rfscore_id>\d+)/$',
        'gsi.views_cs_card_runid_csid.cs_runid_csid_rfscore_edit', name='cs_runid_csid_rfscore_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/remap/(?P<remap_id>\d+)/$',
        'gsi.views_cs_card_runid_csid.cs_runid_csid_remap_edit', name='cs_runid_csid_remap_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/yearfilter/(?P<yf_id>\d+)/$',
        'gsi.views_cs_card_runid_csid.cs_runid_csid_year_filter_edit', name='cs_runid_csid_year_filter_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/collate/(?P<collate_id>\d+)/$',
        'gsi.views_cs_card_runid_csid.cs_runid_csid_collate_edit', name='cs_runid_csid_collate_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/preproc/(?P<preproc_id>\d+)/$',
        'gsi.views_cs_card_runid_csid.cs_runid_csid_preproc_edit', name='cs_runid_csid_preproc_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/mergecsv/(?P<mcsv_id>\d+)/$',
        'gsi.views_cs_card_runid_csid.cs_runid_csid_mergecsv_edit', name='cs_runid_csid_mergecsv_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/rftrain/(?P<rftrain_id>\d+)/$',
        'gsi.views_cs_card_runid_csid.cs_runid_csid_rftrain_edit', name='cs_runid_csid_rftrain_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/randomforest/(?P<rf_id>\d+)/$',
        'gsi.views_cs_card_runid_csid.cs_runid_csid_randomforest_edit', name='cs_runid_csid_randomforest_edit'),


    # card item edit for card sequence // run->csID->card_item
    url(r'^run/card-sequence/(?P<cs_id>\d+)/qrf/(?P<qrf_id>\d+)/$',
        'gsi.views_cs_card_run_csid.cs_run_csid_qrf_edit', name='cs_run_csid_qrf_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/rfscore/(?P<rfscore_id>\d+)/$',
        'gsi.views_cs_card_run_csid.cs_run_csid_rfscore_edit', name='cs_run_csid_rfscore_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/remap/(?P<remap_id>\d+)/$',
        'gsi.views_cs_card_run_csid.cs_run_csid_remap_edit', name='cs_run_csid_remap_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/yearfilter/(?P<yf_id>\d+)/$',
        'gsi.views_cs_card_run_csid.cs_run_csid_year_filter_edit', name='cs_run_csid_year_filter_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/collate/(?P<collate_id>\d+)/$',
        'gsi.views_cs_card_run_csid.cs_run_csid_collate_edit', name='cs_run_csid_collate_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/preproc/(?P<preproc_id>\d+)/$',
        'gsi.views_cs_card_run_csid.cs_run_csid_preproc_edit', name='cs_run_csid_preproc_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/mergecsv/(?P<mcsv_id>\d+)/$',
        'gsi.views_cs_card_run_csid.cs_run_csid_mergecsv_edit', name='cs_run_csid_mergecsv_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/rftrain/(?P<rftrain_id>\d+)/$',
        'gsi.views_cs_card_run_csid.cs_run_csid_rftrain_edit', name='cs_run_csid_rftrain_edit'),


    # processing card
    url(r'^run/card-sequence/processing-card/add$',
        'cards.views.proces_card_new_run', name='proces_card_new_run'),

    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/add$',
        'cards.views.proces_card_runid', name='proces_card_runid'),

    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/$',
        'cards.views.proces_card_runid_csid', name='proces_card_runid_csid'),

    # --------------------------------------------------------------------

    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/add$',
        'cards.views.proces_card_run_new_csid', name='proces_card_run_new_csid'),

    # url(r'^run/new/processing-card/$', 'cards.views.proces_card_new_run', name='proces_card_new_run'),

    # url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/$',
    #     'cards.views.proces_card_sequence_card_edit', name='proces_card_sequence_card_edit'),

    # url(r'^run/(?P<run_id>\d+)/card-sequence/add/processing-card/$',
    #     'cards.views.proces_card_sequence_card_new', name='proces_card_sequence_card_new'),


    # new run cards add
    url(r'^run/card-sequence/processing-card/qrf/add/$', 'cards.views_card_run.new_run_qrf',
        name='new_run_qrf'),
    url(r'^run/card-sequence/processing-card/rfscore/add/$', 'cards.views_card_run.new_run_rfscore',
        name='new_run_rfscore'),
    url(r'^run/card-sequence/processing-card/remap/add/$', 'cards.views_card_run.new_run_remap',
        name='new_run_remap'),
    url(r'^run/card-sequence/processing-card/year-filter/add/$', 'cards.views_card_run.new_run_year_filter',
        name='new_run_year_filter'),
    url(r'^run/card-sequence/processing-card/collate/add/$', 'cards.views_card_run.new_run_collate',
        name='new_run_collate'),
    url(r'^run/card-sequence/processing-card/preproc/add/$', 'cards.views_card_run.new_run_preproc',
        name='new_run_preproc'),
    url(r'^run/card-sequence/processing-card/mergecsv/add/$', 'cards.views_card_run.new_run_mergecsv',
        name='new_run_mergecsv'),
    url(r'^run/card-sequence/processing-card/rftrain/add/$', 'cards.views_card_run.new_run_rftrain',
        name='new_run_rftrain'),

    # new run cards edit
    url(r'^run/card-sequence/processing-card/qrf/(?P<qrf_id>\d+)/$',
        'cards.views_card_run.new_run_qrf_edit', name='new_run_qrf_edit'),
    url(r'^run/card-sequence/processing-card/rfscore/(?P<rfscore_id>\d+)/$',
        'cards.views_card_run.new_run_rfscore_edit', name='new_run_rfscore_edit'),
    url(r'^run/card-sequence/processing-card/remap/(?P<remap_id>\d+)/$',
        'cards.views_card_run.new_run_remap_edit', name='new_run_remap_edit'),
    url(r'^run/card-sequence/processing-card/year-filter/(?P<yf_id>\d+)/$',
        'cards.views_card_run.new_run_year_filter_edit', name='new_run_year_filter_edit'),
    url(r'^run/card-sequence/processing-card/collate/(?P<collate_id>\d+)/$',
        'cards.views_card_run.new_run_collate_edit', name='new_run_collate_edit'),
    url(r'^run/card-sequence/processing-card/preproc/(?P<preproc_id>\d+)/$',
        'cards.views_card_run.new_run_preproc_edit', name='new_run_preproc_edit'),
    url(r'^run/card-sequence/processing-card/mergecsv/(?P<mcsv_id>\d+)/$',
        'cards.views_card_run.new_run_mergecsv_edit', name='new_run_mergecsv_edit'),
    url(r'^run/card-sequence/processing-card/rftrain/(?P<rftrain_id>\d+)/$',
        'cards.views_card_run.new_run_rftrain_edit', name='new_run_rftrain_edit'),


    # new run card-sequenceID cards add
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/qrf/add/$',
        'cards.views_card_run_csid.new_run_csid_qrf', name='new_run_csid_qrf'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/rfscore/add/$',
        'cards.views_card_run_csid.new_run_csid_rfscore', name='new_run_csid_rfscore'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/remap/add/$',
        'cards.views_card_run_csid.new_run_csid_remap', name='new_run_csid_remap'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/year_filter/add/$',
        'cards.views_card_run_csid.new_run_csid_year_filter', name='new_run_csid_year_filter'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/collate/add/$',
        'cards.views_card_run_csid.new_run_csid_collate', name='new_run_csid_collate'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/preproc/add/$',
        'cards.views_card_run_csid.new_run_csid_preproc', name='new_run_csid_preproc'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/mergecsv/add/$',
        'cards.views_card_run_csid.new_run_csid_mergecsv', name='new_run_csid_mergecsv'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/rftrain/add/$',
        'cards.views_card_run_csid.new_run_csid_rftrain', name='new_run_csid_rftrain'),

    # new run card-sequenceID cards edit
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/qrf/(?P<qrf_id>\d+)/$',
        'cards.views_card_run_csid.new_run_csid_qrf_edit', name='new_run_csid_qrf_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/rfscore/(?P<rfscore_id>\d+)/$',
        'cards.views_card_run_csid.new_run_csid_rfscore_edit', name='new_run_csid_rfscore_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/remap/(?P<remap_id>\d+)/$',
        'cards.views_card_run_csid.new_run_csid_remap_edit', name='new_run_csid_remap_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/year_filter/(?P<yf_id>\d+)/$',
        'cards.views_card_run_csid.new_run_csid_year_filter_edit', name='new_run_csid_year_filter_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/collate/(?P<collate_id>\d+)/$',
        'cards.views_card_run_csid.new_run_csid_collate_edit', name='new_run_csid_collate_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/preproc/(?P<preproc_id>\d+)/$',
        'cards.views_card_run_csid.new_run_csid_preproc_edit', name='new_run_csid_preproc_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/mergecsv/(?P<mcsv_id>\d+)/$',
        'cards.views_card_run_csid.new_run_csid_mergecsv_edit', name='new_run_csid_mergecsv_edit'),
    url(r'^run/card-sequence/(?P<cs_id>\d+)/processing-card/rftrain/(?P<rftrain_id>\d+)/$',
        'cards.views_card_run_csid.new_run_csid_rftrain_edit', name='new_run_csid_rftrain_edit'),


    # new runID cards add
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/qrf/add/$',
        'cards.views_card_runid.new_runid_qrf', name='new_runid_qrf'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/rfscore/add/$',
        'cards.views_card_runid.new_runid_rfscore', name='new_runid_rfscore'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/remap/add/$',
        'cards.views_card_runid.new_runid_remap', name='new_runid_remap'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/year-filter/add/$',
        'cards.views_card_runid.new_runid_year_filter', name='new_runid_year_filter'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/collate/add/$',
        'cards.views_card_runid.new_runid_collate', name='new_runid_collate'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/preproc/add/$',
        'cards.views_card_runid.new_runid_preproc', name='new_runid_preproc'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/mergecsv/add/$',
        'cards.views_card_runid.new_runid_mergecsv', name='new_runid_mergecsv'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/rftrain/add/$',
        'cards.views_card_runid.new_runid_rftrain', name='new_runid_rftrain'),


    # new runID cards edit
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/qrf/(?P<qrf_id>\d+)/$',
        'cards.views_card_runid.new_runid_qrf_edit', name='new_runid_qrf_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/rfscore/(?P<rfscore_id>\d+)/$',
        'cards.views_card_runid.new_runid_rfscore_edit', name='new_runid_rfscore_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/remap/(?P<remap_id>\d+)/$',
        'cards.views_card_runid.new_runid_remap_edit', name='new_runid_remap_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/year-filter/(?P<yf_id>\d+)/$',
        'cards.views_card_runid.new_runid_year_filter_edit', name='new_runid_year_filter_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/collate/(?P<collate_id>\d+)/$',
        'cards.views_card_runid.new_runid_collate_edit', name='new_runid_collate_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/preproc/(?P<preproc_id>\d+)/$',
        'cards.views_card_runid.new_runid_preproc_edit', name='new_runid_preproc_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/mergecsv/(?P<mcsv_id>\d+)/$',
        'cards.views_card_runid.new_runid_mergecsv_edit', name='new_runid_mergecsv_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/processing-card/rftrain/(?P<rftrain_id>\d+)/$',
        'cards.views_card_runid.new_runid_rftrain_edit', name='new_runid_rftrain_edit'),


    # new runID card-sequenceID cards add
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/qrf/add/$',
        'cards.views_card_runid_csid.new_runid_csid_qrf', name='new_runid_csid_qrf'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/rfscore/add/$',
        'cards.views_card_runid_csid.new_runid_csid_rfscore', name='new_runid_csid_rfscore'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/remap/add/$',
        'cards.views_card_runid_csid.new_runid_csid_remap', name='new_runid_csid_remap'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/year_filter/add/$',
        'cards.views_card_runid_csid.new_runid_csid_year_filter', name='new_runid_csid_year_filter'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/collate/add/$',
        'cards.views_card_runid_csid.new_runid_csid_collate', name='new_runid_csid_collate'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/preproc/add/$',
        'cards.views_card_runid_csid.new_runid_csid_preproc', name='new_runid_csid_preproc'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/mergecsv/add/$',
        'cards.views_card_runid_csid.new_runid_csid_mergecsv', name='new_runid_csid_mergecsv'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/rftrain/add/$',
        'cards.views_card_runid_csid.new_runid_csid_rftrain', name='new_runid_csid_rftrain'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/randomforest/add/$',
        'cards.views_card_runid_csid.new_runid_csid_randomforest', name='new_runid_csid_randomforest'),


    # new runID card-sequenceID cards edit
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/qrf/(?P<qrf_id>\d+)/$',
        'cards.views_card_runid_csid.new_runid_csid_qrf_edit', name='new_runid_csid_qrf_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/rfscore/(?P<rfscore_id>\d+)/$',
        'cards.views_card_runid_csid.new_runid_csid_rfscore_edit', name='new_runid_csid_rfscore_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/remap/(?P<remap_id>\d+)/$',
        'cards.views_card_runid_csid.new_runid_csid_remap_edit', name='new_runid_csid_remap_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/year_filter/(?P<yf_id>\d+)/$',
        'cards.views_card_runid_csid.new_runid_csid_year_filter_edit', name='new_runid_csid_year_filter_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/collate/(?P<collate_id>\d+)/$',
        'cards.views_card_runid_csid.new_runid_csid_collate_edit', name='new_runid_csid_collate_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/preproc/(?P<preproc_id>\d+)/$',
        'cards.views_card_runid_csid.new_runid_csid_preproc_edit', name='new_runid_csid_preproc_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/mergecsv/(?P<mcsv_id>\d+)/$',
        'cards.views_card_runid_csid.new_runid_csid_mergecsv_edit', name='new_runid_csid_mergecsv_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/rftrain/(?P<rftrain_id>\d+)/$',
        'cards.views_card_runid_csid.new_runid_csid_rftrain_edit', name='new_runid_csid_rftrain_edit'),
    url(r'^run/(?P<run_id>\d+)/card-sequence/(?P<cs_id>\d+)/processing-card/randomforest/(?P<rf_id>\d+)/$',
        'cards.views_card_runid_csid.new_runid_csid_randomforest_edit', name='new_runid_csid_randomforest_edit'),


    # auth
    url(r'^logout/$', auth_views.logout, kwargs={'next_page': 'index'},
        name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='index'),
        name='registration_complete'),
    url(r'^', include('registration.backends.simple.urls', namespace='users')),


    # api
    url(r'^step/(?P<step_id>\d+)/$', 'api.views.update_step', name='update_step'),
    url(r'^run/(?P<run_id>\d+\.\d+\.\d+\.\d+\.\d+)/$', 'api.views.update_run',
        name='update_run'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
