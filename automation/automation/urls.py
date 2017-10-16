from django.contrib import admin
from django.conf.urls import *
from messautomation.views import *


urlpatterns = [
  url(r'^$', main_page),
  url(r'^login/$', login_page),
  url(r'^logout/$', logout_view),
  # url(r'^extra_login/$', extra_login),
  url(r'^(?P<rollnumber>[0-9{6}]+)/item_extra/$', item_extra),
  url(r'^(?P<tokennum>[0-9{6}]+)/token/$', token_generator),
  url(r'^(?P<rollnumber>[0-9{6}]+)/changepassword/$', changepassword),
  url(r'^student_view/$', student_view),
  url(r'^token_detail/$', token_view),
  url(r'^mess/$', mess_view),
  url(r'^delete/$', delete_all),
  url(r'^backup/$', backup_data),
  url(r'^signup/$', signup_view),
  url(r'^forgotpass/$', forgot_password),
  url(r'^admin/', include(admin.site.urls)),
  ]