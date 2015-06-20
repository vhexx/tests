from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response
from tests.models import TestPrototype


def test(request):
    test_id = request.GET.get('id')
    try:
        test_instance = TestPrototype.objects.get(id=test_id)
    except Exception:
        return HttpResponseNotFound('Такого теста не существует')
    context = {
        'test_title': test_instance.title
    }
    return render_to_response('test.html', context)


def question(request):
    id = request.GET.get('id')
    return render_to_response('question.html')