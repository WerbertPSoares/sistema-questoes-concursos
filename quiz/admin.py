from django.contrib import admin
from .models import Disciplina, Questao, Alternativa, RespostaUsuario, Simulado

class AlternativaInline(admin.TabularInline):
    model = Alternativa
    extra = 4  # número de alternativas que vão aparecer por padrão

class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('enunciado', 'disciplina', 'banca', 'ano', 'nivel')
    search_fields = ('enunciado',)
    list_filter = ('disciplina', 'banca', 'ano', 'nivel')
    inlines = [AlternativaInline]

admin.site.register(Disciplina)
admin.site.register(Questao, QuestaoAdmin)
admin.site.register(RespostaUsuario)
admin.site.register(Simulado)
