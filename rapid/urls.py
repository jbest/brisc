from django.conf.urls import patterns, url

from rapid import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^new/$', views.new_inventory, name='new_inventory'),
    url(r'^(?P<pk>\d+)/$', views.InventoryDetail.as_view(), name='inventory_detail'),
    url(r'^(?P<pk>\d+)/stats$', views.InventoryStats.as_view(), name='inventory_stats'),
    url(r'^(?P<pk>\d+)/stats/export$', views.InventoryStatsCSV, name='inventory_stats_export'),
    # Can't get this URL pattern to work for some reason
    #url(r'^(?P<pk>\d+)/new_session/$', views.new_session, name='new_session'),
    url(r'^new_session/$', views.new_session, name='new_session'),
    url(r'^session/(?P<pk>\d+)/$', views.SessionDetail.as_view(), name='session_detail'),
    url(r'^session/end/$', views.end_session, name='end_session'),
    url(r'^taxon/new/$', views.new_taxon, name='new_taxon'),  # AJAX call from modal forms
    url(r'^count/$', views.taxa, {'mode': 'create'}, name='count'),
    url(r'^count/(?P<pk>\d+)/$', views.TaxonSetDetail.as_view(), name='count_detail'),
    url(r'^count/(?P<pk>\d+)/edit/$', views.taxa, {'mode': 'edit'}, name='count_edit'),
    url(r'^taxa/group/$', views.taxa_in_taxon, {'taxon_rank': 'group'}, name='taxa_in_group_base'),
    url(r'^taxa/group/(?P<taxon_id>\d+)/$', views.taxa_in_taxon, {'taxon_rank': 'group'}, name='taxa_in_group'),
    url(r'^taxa/family/$', views.taxa_in_taxon, {'taxon_rank': 'family'}, name='taxa_in_family_base'),
    url(r'^taxa/family/(?P<taxon_id>\d+)/$', views.taxa_in_taxon, {'taxon_rank': 'family'}, name='taxa_in_family'),
    url(r'^taxa/genus/$', views.taxa_in_taxon, {'taxon_rank': 'genus'}, name='taxa_in_genus_base'),
    url(r'^taxa/genus/(?P<taxon_id>\d+)/$', views.taxa_in_taxon, {'taxon_rank': 'genus'}, name='taxa_in_genus'),
)
