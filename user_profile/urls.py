from django.urls import path

from . import views

urlpatterns = [
    path('policy_count/', views.total_policy_count_for_user, name='policy_count'),
    path('days_active/', views.total_days_active_for_user, name='days_active'),
    path('new_users/', views.total_new_users_count_for_date, name='new_users'),
    path('lapsed_users/', views.total_lapsed_users_count_for_month, name='lapsed_users'),
    path('new_users_premium/', views.total_new_users_premium_per_date_for_underwriter, name='new_users_premium'),
    path('policies/', views.get_policies, name='policies'),
]
