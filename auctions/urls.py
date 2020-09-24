from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("catgory/", views.index, name="category"),
    path("catgory/<str:category>", views.index, name="category"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("new_listing/", views.new_listing, name="new_listing")
]
