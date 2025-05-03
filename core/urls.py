from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:provider_id>/', views.book_provider, name='book_provider'),
    path('success/', views.booking_success, name='booking_success'),
    path('bookings/', views.view_bookings, name='view_bookings'),
    # ↓ new ones:
    path('signup/', views.signup, name='signup'),
    path('login/',  views.login_view,  name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('review/<int:booking_id>/', views.leave_review, name='leave_review'),
    # Merge these two paths
    path('provider-reviews/<int:provider_id>/', views.provider_reviews, name='provider_reviews'),
]
