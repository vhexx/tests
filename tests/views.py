from random import shuffle
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from tests.models import PreQuestion, Test, Answer, PostQuestion, ImagePair, Image
from .const import prequestions_state, postquestions_state, pairs_state, initial_state


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
    request.session['state'] = initial_state

    # retrieve image pairs, shuffle them and put in session
    image_pair_ids = prepare_images(test_id)
    request.session['image_pair_ids'] = image_pair_ids
    request.session['image_pair_id_ptr'] = -1

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


def question(request, question_id):
    state = request.session.get('state')

    if state == initial_state:
        request.session['state'] = prequestions_state

    test_id = request.session.get('test_id')
    if test_id is None:
        return HttpResponseNotFound('Вопрос недоступен')

    if request.session.get('state') == prequestions_state:
        model = PreQuestion
    elif request.session.get('state') == postquestions_state:
        model = PostQuestion
    else:
        return HttpResponseNotFound('Вопрос недоступен')

    questions = model.objects.filter(test=test_id).order_by('order')

    if len(questions) == 0:
        return HttpResponseNotFound('Вопросов к этому тесту не найдено')

    if question_id not in questions:
        return HttpResponseNotFound('Вопрос недоступен')

    prev_id = None
    next_id = None
    go_to_pairs = False

    # determine next and previous question
    for i in range(0, len(questions)):
        if questions[i].id == int(question_id):
            question_instance = questions[i]
            if i != 0:
                prev_id = questions[i - 1].id
            if i != len(questions) - 1:
                next_id = questions[i + 1].id
            else:
                if model == PreQuestion:
                    go_to_pairs = True

            context = {
                'question_title': question_instance.title,
                'answers': Answer.objects.filter(question=question_id),
                'prev_id': prev_id,
                'next_id': next_id,
                'go_to_pairs': go_to_pairs
            }
            return render_to_response('question.html', context)

    return HttpResponseNotFound('Такого вопроса не существует')


def pairs(request):
    if request.session.get('state') != pairs_state:
        return HttpResponseNotFound('Страница недоступна')

    image_pair_ids = request.session.get('image_pair_ids')

    ptr = request.session.get('image_pair_id_ptr') + 1
    if ptr > len(image_pair_ids) - 1:
        return HttpResponseNotFound('Пикчи кончились')

    request.session['image_pair_id_ptr'] = ptr
    image_pair = ImagePair.objects.get(id=image_pair_ids[ptr])
    left = '/media/' + str(Image.objects.get(id=image_pair.left).img)
    right = '/media/' + str(Image.objects.get(id=image_pair.right).img)

    context = {
        'left': left,
        'right': right
    }
    return render_to_response('image_pair.html', context)


def go_to_pairs(request):
    if request.session.get('state') == prequestions_state:
        request.session['state'] = pairs_state
        return redirect('/pairs')
    else:
        return HttpResponseNotFound('Страница недоступна')
