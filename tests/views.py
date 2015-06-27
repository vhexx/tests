from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response, redirect
from tests.models import PreQuestion, Test, Answer, PostQuestion
from .const import prequestions_state


def index(requst):
    return redirect('/admin')


def test(request):
    print(dict(request.session))
    test_id = int(request.GET.get('id'))
    try:
        test_instance = Test.objects.get(id=test_id)
    except Exception:
        return HttpResponseNotFound('Такого теста не существует')

    # put current test id in session
    request.session['test_id'] = test_id
    request.session['state'] = prequestions_state

    # retrieve related questions and put them in session
    prequestions = PreQuestion.objects.filter(test=test_id).order_by('order')

    context = {
        'test_title': test_instance.title,
        'question_id': prequestions[0]
    }
    return render_to_response('test.html', context)


def question(request):
    question_id = request.GET.get('id')
    try:
        question_instance = PreQuestion.objects.get(id=question_id)
    except Exception:
        return HttpResponseNotFound('Такого вопроса не существует')

    context = {
        'question_title': question_instance.title,
        'answers': Answer.objects.filter(question=question_id)
    }
    return render_to_response('question.html', context)