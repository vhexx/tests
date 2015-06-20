from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response
from tests.models import TestPrototype, QuestionPrototype


def test(request):
    print(dict(request.session))
    test_id = request.GET.get('id')
    try:
        test_instance = TestPrototype.objects.get(id=test_id)
    except Exception:
        return HttpResponseNotFound('Такого теста не существует')

    #put current test id in session
    request.session['test_id'] = test_id

    #retrieve related questions and put them in session
    related_questions = QuestionPrototype.objects.filter(test=test_id)
    question_list = []
    for q in related_questions:
        question_list.append(q.id)

    request.session['question_ids'] = list

    context = {
        'test_title': test_instance.title
    }
    return render_to_response('test.html', context)


def question(request):
    id = request.GET.get('id')
    return render_to_response('question.html')