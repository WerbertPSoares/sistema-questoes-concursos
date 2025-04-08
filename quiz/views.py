from django.shortcuts import render, get_object_or_404, redirect
from .models import Questao, RespostaUsuario, Alternativa
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
import random
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

@login_required
def quiz(request):
    # lógica do quiz
    pass

@login_required
def flashcards_view(request):
    # lógica dos flashcards
    pass

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz/login')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/register.html', {'form': form})

def flashcards_view(request):
    questoes = Questao.objects.all()

    if questoes:
        questao = random.choice(questoes)
    else:
        questao = None

    return render(request, 'quiz/flashcards.html', {'questao': questao})

def pagina_inicial(request):
    return render(request, 'quiz/index.html')


@login_required
def quiz(request):
    # Filtra todas as questões disponíveis
    questoes = Questao.objects.all()

    # Pega uma questão aleatória
    if questoes.exists():
        questao = random.choice(questoes)
    else:
        questao = None

    context = {'questao': questao}
    return render(request, 'quiz/quiz.html', context)

@login_required
def responder(request, questao_id):
    questao = get_object_or_404(Questao, id=questao_id)

    if request.method == 'POST':
        alternativa_id = request.POST.get('alternativa')
        alternativa = get_object_or_404(Alternativa, id=alternativa_id)

        # Salva a resposta do usuário
        RespostaUsuario.objects.create(
            usuario=request.user,
            questao=questao,
            alternativa=alternativa
        )

        # Verifica se a resposta está correta
        if alternativa.correta:
            resultado = 'Correto!'
        else:
            resultado = 'Incorreto!'

        return render(request, 'quiz/resultado.html', {'resultado': resultado, 'questao': questao, 'alternativa': alternativa})

    return redirect('quiz')

@login_required
def relatorio(request):
    usuario = request.user

    total_respondidas = RespostaUsuario.objects.filter(usuario=usuario).count()
    total_corretas = RespostaUsuario.objects.filter(usuario=usuario, alternativa__correta=True).count()
    total_erradas = RespostaUsuario.objects.filter(usuario=usuario, alternativa__correta=False).count()

    # Porcentagem de acertos
    if total_respondidas > 0:
        porcentagem_acertos = (total_corretas / total_respondidas) * 100
    else:
        porcentagem_acertos = 0

    # Acertos por disciplina
    acertos_por_disciplina = (
        RespostaUsuario.objects.filter(usuario=usuario, alternativa__correta=True)
        .values('questao__disciplina__nome')
        .annotate(total=Count('id'))
    )

    # Acertos por banca
    acertos_por_banca = (
        RespostaUsuario.objects.filter(usuario=usuario, alternativa__correta=True)
        .values('questao__banca')
        .annotate(total=Count('id'))
    )

    # Acertos por dificuldade
    acertos_por_dificuldade = (
    RespostaUsuario.objects.filter(usuario=usuario, alternativa__correta=True)
    .values('questao__nivel')
    .annotate(total=Count('id'))
)


    context = {
        'total_respondidas': total_respondidas,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'porcentagem_acertos': porcentagem_acertos,
        'acertos_por_disciplina': acertos_por_disciplina,
        'acertos_por_banca': acertos_por_banca,
        'acertos_por_dificuldade': acertos_por_dificuldade,
    }

    return render(request, 'quiz/relatorio.html', context)