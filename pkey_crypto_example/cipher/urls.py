from django.conf.urls import patterns, url
from cipher import views


urlpatterns = patterns('cipher.views',
    # url(r'^$', 'pkey_crypto_example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^register/$', views.PublicKeyList.as_view()),
)
