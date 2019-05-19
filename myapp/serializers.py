from rest_framework import serializers
from .models import Categoria, Produto, Pedido, Estoque


class CategoriaSerializers(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = '__all__'


class ProdutoSerializers(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = '__all__'


class PedidoSerializers(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ('produtos',)

    produtos = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all(), many=True)

    def validate_produtos(self, produtos):

        categorias = Categoria.objects.all()

        for produto in produtos:
            if produto.estoque.quantidade == 0:
                raise serializers.ValidationError(
                    (str(produto.especificacao) + ' sem estoque')
                )

        for categoria in categorias:
            contador = 0
            for produto in produtos:
                if produto.categoria.id == categoria.id:
                    contador = contador + 1
            if contador == 0:
                raise serializers.ValidationError(
                    ('Não há produto na categoria ' + str(categoria.nome))
                )
            elif contador > 1:
                raise serializers.ValidationError(
                    ('Somente um produto por categoria')
                )

        return produtos


class PedidoListSerializers(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ('preco', 'produtos', 'id', 'card', 'status')


class EstoqueSerializers(serializers.ModelSerializer):

    class Meta:
        model = Estoque
        fields = '__all__'

