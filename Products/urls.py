from views import index, all_products
from django.conf.urls import url



urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^products$', all_products, name='products')
]