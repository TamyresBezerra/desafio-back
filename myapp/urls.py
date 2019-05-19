from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^categorias/$', views.CategoriaList.as_view(), name='categoria-list'),
    url(r'^categoria/(?P<pk>[0-9]+)/$', views.CategoriaDetail.as_view(), name='categoria-detail'),

    url(r'^produtos/$', views.ProdutoList.as_view(), name='produto-list'),
    url(r'^produto/(?P<pk>[0-9]+)/$', views.ProdutoDetail.as_view(), name='produto-detail'),

    url(r'^pedidos/$', views.PedidoList.as_view(), name='pedido-list'),
    url(r'^pedido/(?P<pk>[0-9]+)/$', views.PedidoDetail.as_view(), name='pedido-detail'),

    url(r'^estoques/$', views.EstoqueList.as_view(), name='pedido-detail'),
    url(r'^estoque/(?P<pk>[0-9]+)/$', views.EstoqueDetail.as_view(), name='pedido-detail'),
]

