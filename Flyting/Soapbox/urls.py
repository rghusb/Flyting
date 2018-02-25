from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'Soapbox'

urlpatterns = [
    path("conv/<int:soap_pk>/", views.ConvincedView.as_view(), name="convinced"),
    path("<int:pk>", views.SoapboxDetailView.as_view(), name="soapbox-detail"),
    path("for/<int:art_pk>/new/", views.SoapboxCreateView.as_view(), name="soapbox-create"),
    path("for/<int:soap_pk>/new/rebuttal/<int:reb_pk>/", views.RebuttalCreateView.as_view(), name="rebuttal-reply-create"),
    path("for/<int:soap_pk>/new/rebuttal/", views.RebuttalCreateView.as_view(), name="rebuttal-create"),
    path("user/<int:user_pk>/all/", views.SoapboxUserListView.as_view(), name="soapbox-user-list"),
    path("for/<int:art_pk>/", views.SoapboxArtListView.as_view(), name="soapbox-art-list"),
    path("downvote/", views.DownvoteView, name="downvote"),
    path("upvote/", views.UpvoteView, name="upvote"),
    path("rebuttal/downvote/", views.RebuttalDownvoteView, name="rebuttal-downvote"),
    path("rebuttal/upvote/", views.RebuttalUpvoteView, name="rebuttal-upvote"),
]
