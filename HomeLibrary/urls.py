from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HomeLibrary.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('library.views',
                        (r'^$', 'index'),
                        (r'^login/$', 'user_login'),
                        (r'^logout/$', 'user_logout'),
                        # (r'^home/$', 'index'),
                        (r'^user/(?P<user_id>\d+)/$', 'view_user_profile'),
                        (r'^book/(?P<book_id>\d+)/$', 'view_book'),
                        (r'^books/$', 'view_all_book'),
                        (r'^author/(?P<author_id>\d+)/$', 'view_author'),
                        (r'^publisher/(?P<publisher_id>\d+)/$', 'view_publisher'),
                        (r'^add_book/$', 'add_book'),
                        (r'^add_author/$', 'add_author'),
                        (r'^add_publish_house/$', 'add_publish_house'),
                        )
