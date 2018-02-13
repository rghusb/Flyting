from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'Articles'

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="articles-list"),
    path("new/", views.CreateArticleView.as_view(), name="create"),
    path("<int:pk>/",views.ArticleDetailView.as_view(),name="article-detail"),
    path("<int:pk>/delete/",views.DeleteArticleView.as_view(),name="delete"),
    path("<int:article_id>/vote/", views.VoteRedirectView.as_view(), name="vote-redirect"),
    path("<int:article_id>/vote/<int:choice_id>/by/<int:user_id>/", views.VoteRedirectView.as_view(), name="vote-argh"),
    path("vote", views.VoteView, name="vote"),
]
