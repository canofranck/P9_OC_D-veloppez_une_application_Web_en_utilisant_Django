"""
URL configuration for LITRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView,LogoutView
import authentication.views
import review.views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('home/', review.views.home, name='home'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('profile_photo/upload/', authentication.views.upload_profile_photo,name='upload_profile_photo'),
    path('ticket/create/', review.views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/edit/', review.views.edit_ticket, name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete/', review.views.delete_ticket, name='delete_ticket'),
    path('ticket/<int:ticket_id>/error_delete_ticket/', review.views.error_delete_ticket, name='error_delete_ticket'),
    path('ticket/<int:ticket_id>/review/create/', review.views.create_review, name='create_review'),
    path('ticket/<int:ticket_id>/review/<int:review_id>/edit/',review.views.edit_review, name='edit_review'),
    path('ticket/<int:ticket_id>/review/<int:review_id>/delete/',review.views.delete_review, name='delete_review'),
    path('ticket/<int:ticket_id>/detail/',review.views.ticket_detail, name='ticket_detail'),
    path('ticket/<int:ticket_id>/review/<int:review_id>/detail/',review.views.review_detail, name='review_detail'),
    path('follow-users/listing/',review.views.follow_users, name='follow_users'),
    path('follow-users/<str:followed_user>/delete', review.views.delete_follow, name='delete_follow'),
    path('ticket/create_ticket_and_review/', review.views.create_ticket_and_review,
         name='create_ticket_and_review'),    
    path('post-edit/', review.views.post_edit, name='post_edit'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
