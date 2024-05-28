from django.conf.urls import url, include

from clientes.views import *

urlpatterns = [
    url(r'^clientes/$', clientes),
    url(r'^clientes/(?P<pk>\w+)/$', clientesDetail)
]