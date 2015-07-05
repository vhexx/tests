from random import shuffle
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from tests.models import PreQuestion, Test, Answer, PostQuestion, ImagePair
from .const import prequestions_state


def index(requst):
    return redirect('/admin')


def test(request, test_id):
    print(dict(request.session))
    try:
        test_instance = Test.objects.get(id=test_id)

    except Exception:
        return HttpResponseNotFound('Такого теста не существует')

    # put current test id in session
    request.session['test_id'] = test_id
    request.session['state'] = prequestions_state

    # retrieve image pairs, shuffle them and put in session
    image_pair_ids = prepare_images(test_id)
    request.session['image_pair_ids'] = image_pair_ids

    # retrieve related questions and put them in session
    prequestions = PreQuestion.objects.filter(test=test_id).order_by('order')
    context = {
        'test_title': test_instance.title,
        'question_id': prequestions[0].id if len(prequestions) > 0 else 0
    }
    return render_to_response('test.html', context)


def prepare_images(test_id):
    image_pairs = ImagePair.objects.filter(test=test_id)
    image_pair_ids = []
    for pair in image_pairs:
        for i in range(pair.repeats):
            image_pair_ids.append(pair.id)
    shuffle(image_pair_ids)
    return image_pair_ids

def question(request, question_id, model):
    test_id = request.session.get('test_id')
    if test_id is None:
        return HttpResponseNotFound('Вопрос недоступен')

    prequestions = model.objects.filter(test=test_id).order_by('order')

    if len(prequestions) == 0:
        return HttpResponseNotFound('Вопросов к этому тесту не найдено')

    prev_id = None
    next_id = None

    #determine next and previous question
    for i in range(0, len(prequestions)):
        if prequestions[i].id == int(question_id):
            question_instance = prequestions[i]
            if i != 0:
                prev_id = prequestions[i - 1].id
            if i != len(prequestions) - 1:
                next_id = prequestions[i + 1].id

            context = {
                'question_title': question_instance.title,
                'answers': Answer.objects.filter(question=question_id),
                'prev_id': prev_id,
                'next_id': next_id
            }
            return render_to_response('question.html', context)

    return HttpResponseNotFound('Такого вопроса не существует')


def prequestion(request, question_id):
    return question(request, question_id, PreQuestion)

def postquestion(request, question_id):
    return question(request, question_id, PostQuestion)
