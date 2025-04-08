from django.db import models
from django.contrib.auth.models import User

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Questao(models.Model):
    NIVEL_DIFICULDADE = (
        ('Fácil', 'Fácil'),
        ('Médio', 'Médio'),
        ('Difícil', 'Difícil'),
    )

    enunciado = models.TextField()
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    banca = models.CharField(max_length=100)
    ano = models.PositiveIntegerField()
    nivel = models.CharField(max_length=10, choices=NIVEL_DIFICULDADE)

    def __str__(self):
        return f"{self.enunciado[:50]}..."

class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, related_name='alternativas', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    correta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto

class RespostaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    respondido_em = models.DateTimeField(auto_now_add=True)

class Simulado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    questoes = models.ManyToManyField(Questao)

    def __str__(self):
        return f"Simulado {self.id} - {self.usuario.username}"
