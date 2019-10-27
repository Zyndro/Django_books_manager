from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add/book/$', views.add_book, name='add_book'),
    url(r'^import/book/$', views.google_import, name='import_book'),
]