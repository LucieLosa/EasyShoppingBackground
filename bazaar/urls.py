from django.urls import path

from bazaar import views

urlpatterns = [
    path("", views.EventsList.as_view()),
    path("detail/<int:pk>/", views.EventDetail.as_view()),
    path("add-cart/<str:cartId>/", views.AddCart.as_view()),
]
