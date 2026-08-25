from django.urls import path

from reconciliation import views


urlpatterns = [
    path("orgs/", views.organizations, name="organizations"),
    path(
        "disagreements/",
        views.disagreements,
        name="disagreements",
    ),
]