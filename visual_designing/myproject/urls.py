"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myapp import views  # Import your views from the app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('adduserdetail', views.adduserdetail, name='adduserdetail'),
    path('showuser', views.showuser, name='showuser'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('update', views.update, name='update'),
    path('add_desingner', views.add_desingner, name='add_desingner'),
    path('showdesigner', views.showdesigner, name='showdesigner'),
    path('edit_designer', views.edit_designer, name='edit_designer'),
    path('updatedesigner', views.updatedesigner, name='updatedesigner'),
    path('addrequirements', views.addrequirements, name='addrequirements'),
    path('adddesign', views.adddesign, name='adddesign'),
    path('showdesigners', views.showdesigners, name='showdesigners'),
    path('showrequirements', views.showrequirements, name='showrequirements'),
    path('myrequirements', views.myrequirements, name='myrequirements'),
    path('product/<int:product_id>/', views.single_property, name='single_property'),
    path('place-bid/<int:product_id>/', views.place_bid, name='place_bid'),
    path('manage-bids/<int:product_id>/', views.manage_bids, name='manage_bids'),
    path('designer_bids', views.designer_bids, name='designer_bids'),
    path('success', views.success, name='success'),
    path('portfolio_view/<int:designer_id>/', views.portfolio_view, name='portfolio_view'),
    path('pay_status', views.pay_status, name='pay_status'),
    path('showfeedback', views.showfeedback, name='showfeedback'),
    path('complaint_submit', views.complaint_submit, name='complaint_submit'),
    path('booking_desinger', views.booking_desinger, name='booking_desinger'),
    path('booking_by_user', views.booking_by_user, name='booking_by_user'),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
