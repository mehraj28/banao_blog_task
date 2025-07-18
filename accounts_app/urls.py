from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.home, name='home'),
                  path('signup/patient/', views.patient_signup, name='patient_signup'),
                  path('signup/doctor/', views.doctor_signup, name='doctor_signup'),
                  path('login/', views.login_view, name='login'),
                  path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
                  path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
                  path('logout/', views.logout_view, name='logout'),
                  path('blog/create/', views.create_blog_post, name='create_blog_post'),
                  path('edit/<int:post_id>/', views.edit_blog_post, name='edit_blog_post'),
                  path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
                  path('appointment_details/<int:appointment_id>/', views.appointment_details, name='appointment_details'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
