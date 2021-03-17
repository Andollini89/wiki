from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('watchlist', views.watchlist,name='watchlist'),
    path('create', views.new_listing, name='new_listing'),
    path('listings/object/<str:listing_id>',views.listing, name='listing'),
    path('category/filter/<str:cat_id>', views.categories, name='categories'),
    path('add_category',views.add_category, name='add_category'),
    path('new_bid/<str:l_id>', views.new_bid, name='new_bid'),
    path('comments/<str:l_id>', views.comments, name= 'comments'),
    path('status<str:l_id>', views.close_auction, name='status_change'),
    path('user/watchlist/<str:l_id>', views.add_to_watchlist, name='add_to_watchlist')
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

