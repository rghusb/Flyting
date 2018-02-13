from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'Soapbox'

urlpatterns = [
    path("<int:pk>", views.SoapboxDetailView.as_view(), name="soapbox-detail"),
    path("new/", views.SoapboxCreateView.as_view(), name="soapbox-create"),
    path("all/", views.SoapboxListView.as_view(), name="soapbox-list"),
    path("for/<int:art_pk>/", views.SoapboxArtListView.as_view(), name="soapbox-art-list"),
]
