from views import all_products, index
from django.conf.urls import url


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^products$', all_products, name='products'),
]