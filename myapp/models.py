from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):

    class Meta:
        db_table = 'categoria'

    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Produto(models.Model):

    class Meta:
        db_table = 'produto'

    especificacao = models.TextField()
    preco = models.DecimalField(max_digits=7, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.especificacao


class Estoque(models.Model):
    class Meta:
        db_table = 'estoque'

    quantidade = models.IntegerField()
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)

    def __str__(self):
        return self.quantidade


class Pedido(models.Model):

    class Meta:
        db_table = 'pedido'

    preco = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=200)
    produtos = models.ManyToManyField(Produto)
    card = models.CharField(max_length=200, default=" ")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.produtos
