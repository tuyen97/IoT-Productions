from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

import uuid
from . import views, apis
from . import models

urlpatterns = [
    path('', views.index, name='index'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('devices-info/', views.devices_info, name='devices-info'),
    path('warning/', views.warning, name='warning'),
    path('members-info/', views.members_info, name='members-info'),
    re_path(r'^member-profile/', views.member_profile, name='member-profile'),
    re_path(r'^member/train/', views.train_face),
    path('api/member/', views.member_api, name='api/member'),
    path('api/change-card-id/', views.change_card_id, name='api/change-card-id'),
    path('api/upload_video/', views.upload_video, name='api/upload_video'),
    path('api/server-auth/', views.server_authentication, name='api/server-auth'),
    path('calculate_hour/', apis.calculate_hour, name='calculate_hour'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('server_log/',views.server_log, name='server_log'),
    path('server_log_stat', views.server_log_stat, name='server_log_stat'),
    path('test/', apis.test)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

user = models.Member(id = uuid.uuid4(),
                     name="tuyen",
                     email="tuyen@hpcc.com",
                     card_id="1A 2B 3C",
                     course="iot",
                     research_about="iot",
                     coefficient="1",
                     position= "TE")
try:
    u = models.Member.objects.get(email="tuyen@hpcc.com", password="password")
except models.Member.DoesNotExist:
    user.save()