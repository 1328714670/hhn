from django.urls import re_path

from customer import views

app_name='customer'

urlpatterns = [

    re_path('^login_judge/$',views.login_judge.as_view(),name='login_judge'),
    re_path('^worker_information$', views.worker_information_ok.as_view(), name='worker_information'),
    re_path('^worker_information/$', views.worker_information_ok.as_view(), name='worker_information-ok'),

    re_path('^worker_logout/$',views.worker_logout.as_view(),name='worker_logout'),
    re_path('^worker_change_worker_password/$',views.worker_change_worker_password.as_view(),name='worker_change_worker_password'),

    re_path('^worker_finance_infomation/$',views.worker_finance_infomation.as_view(),name='worker_finance_infomation'),
    re_path('^worker_order_record/$',views.finance_infomation.as_view(),name='finance_infomation'),

]


