from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Categoria, Produto, Pedido, Estoque
from .serializers import CategoriaSerializers, ProdutoSerializers, PedidoSerializers, PedidoListSerializers, EstoqueSerializers
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, DjangoModelPermissions
from django_filters import rest_framework as filters
from trello import TrelloApi


def cad_pedido_trello(dados, valor_total):
    trello = TrelloApi('3e07bd7f00974e1c71db3f0d30f3d50c', '55fb23e337aa599c137b1d23c225d1f5825a6274bf010c525a5c43ffe200b906')
    produtos = " "
    for produto in dados.produtos.all():
        produtos = produtos+'\n'+str(produto)
    card = trello.cards.new('Pedido ' + str(dados.id), '5cdeee36a3d935459b57d978', 'Cliente: \n\n' + 'nome: ' + str(dados.user.username) + '\n' + 'email: ' + str(dados.user.email) + '\n\n' + 'Componentes: \n' + produtos + '\n\n' + 'Valor Total: ' + str(valor_total))
    return card['id']


class CategoriaList(generics.ListCreateAPIView):

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializers
    authentication_classes = [SessionAuthentication, TokenAuthentication,]
    permission_classes = (DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = '__all__'


class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializers
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = '__all__'


class ProdutoList(generics.ListCreateAPIView):

    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializers
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = (DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = '__all__'


class ProdutoDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializers
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = (DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = '__all__'


class PedidoList(generics.ListCreateAPIView):

    #queryset = Pedido.objects.all()
    serializer_class = PedidoSerializers
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = '__all__'

    def create(self, request, *args, **kwargs):

        serializer = PedidoSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        valor_total = 0
        dados = serializer.save(user=request.user, preco=0)

        for produto in dados.produtos.all():
            produto.estoque.quantidade = produto.estoque.quantidade - 1
            valor_total = valor_total + produto.preco
            produto.estoque.save()

        id_card = cad_pedido_trello(dados, valor_total)
        serializer.save(card=id_card, preco=valor_total)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = PedidoListSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PedidoListSerializers(queryset, many=True)

        trello = TrelloApi('3e07bd7f00974e1c71db3f0d30f3d50c', '55fb23e337aa599c137b1d23c225d1f5825a6274bf010c525a5c43ffe200b906')

        for pedido in serializer.data:
            card = trello.cards.get(pedido["card"])
            lista = trello.lists.get(card["idList"])
            pedido["status"] = lista["name"]
        return Response(serializer.data)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Pedido.objects.all()
        else:
            return Pedido.objects.all().filter(user=self.request.user)


class PedidoDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializers
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = '__all__'


class EstoqueList(generics.ListCreateAPIView):

    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializers
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = '__all__'


class EstoqueDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializers
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = '__all__'