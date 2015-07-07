from random import shuffle
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response, redirect
from django.db import connection
import time
from tests.models import PreQuestion, Test, Answer, PostQuestion, ImagePair, TrainingImagePair, Question, \
    UserQuestionResults, UserImagePairResults
from .const import prequestions_state, postquestions_state, pairs_state, training_state, initial_state
from tests.utils.check_results import check_question_results, check_image_pair_results


def index(requst):
    return redirect('/admin')


def test(request, test_id):
    try:
        test_instance = Test.objects.get(id=test_id)

    except Exception:
        return HttpResponseNotFound('Такого теста не существует')

    # put current test id in session
    request.session['start_time'] = int(time.time())
    request.session['test_id'] = test_id
    request.session['state'] = prequestions_state

    # retrieve image pairs, shuffle them and put in session
    image_pair_ids = prepare_images(test_id)
    request.session['image_pair_ids'] = image_pair_ids
    request.session['image_pair_id_ptr'] = -1

    # retrieve related questions and put them in session
    prequestions = PreQuestion.objects.filter(test=test_id).order_by('order')

    context = {
        'test_title': test_instance.title,
        'question_id': next((q.id for q in prequestions if not q.isSeparator), None),
        'test_description': test_instance.description
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
    if check_question_results(request):
        return failed(request)
    question_id = int(question_id)

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

    if question_id not in list(map(lambda q: q.id, questions)):
        return HttpResponseNotFound('Вопрос недоступен')

    separator_found = False
    first_found = False
    prev_id = None
    next_id = None

    actual_questions = []

    for i in range(0, len(questions)):
        if questions[i].isSeparator:
            if not first_found:
                continue
            else:
                separator_found = True
        else:
            if separator_found:
                next_id = questions[i].id
                break
            else:
                if questions[i].id == question_id:
                    actual_questions.append(questions[i])
                    first_found = True
                    if questions[i].id == prev_id:
                        prev_id = None
                else:
                    if first_found:
                        actual_questions.append(questions[i])
                    else:
                        if i == 0:
                            prev_id = questions[i].id
                        elif questions[i - 1].isSeparator:
                            prev_id = questions[i].id

    if not first_found == 1:
        return HttpResponseNotFound('Такого вопроса не существует')

    questions_and_answers = []

    for q in actual_questions:
        questions_and_answers.append((q, Answer.objects.filter(question=q.id)))

    cursor = connection.cursor()
    cursor.execute('''select count(*)
                        from (select question_id
                                from tests_userquestionresults
                                group by question_id, session_key_id, start_time
                                having session_key_id=%s
                                and start_time=%s) as q''',
                   [request.session.session_key, int(request.session.get('start_time'))])
    question_passed = cursor.fetchone()[0]

    question_instance = model.objects.get(id=question_id)
    context = {
        'titles': question_instance.title,
        'qa': questions_and_answers,
        'prev_id': prev_id,
        'next_id': next_id,
        'question_ration':
            100 * float(question_passed) / Question.objects.filter(test=test_id).count() if not 0 else 1,
        'is_postquestion': True if model == PostQuestion else False
    }
    return render_to_response('question.html', context)


def before_training(request):
    if check_question_results(request):
        return failed(request)
    request.session['state'] = training_state
    training_image_pairs = TrainingImagePair.objects.all().order_by('id')
    context = {
        'training_image_pair_id': training_image_pairs[0].id if len(training_image_pairs) > 0 else 0
    }
    return render_to_response('before_training.html', context)


def training(request, training_image_pair_id):
    training_image_pair_id = int(training_image_pair_id)

    test_id = request.session.get('test_id')
    seconds = Test.objects.get(id=test_id).seconds if not None else -1

    training_image_pairs = TrainingImagePair.objects.all().order_by('id')

    for i in range(0, len(training_image_pairs)):
        if training_image_pairs[i].id == training_image_pair_id:
            if i != len(training_image_pairs) - 1:
                next_training_image_pair_id = training_image_pairs[i + 1].id
            else:
                next_training_image_pair_id = None

            context = {
                'text': training_image_pairs[i].text,
                'left': '/media/' + str(training_image_pairs[i].left),
                'right': '/media/' + str(training_image_pairs[i].right),
                'next_training_image_pair': next_training_image_pair_id,
                'seconds': seconds,
                'is_training': True
            }
            return render_to_response('image_pair.html', context)
    return HttpResponseNotFound('Страница недоступна')


def after_training(request):
    test_id = request.session.get('test_id')
    seconds = Test.objects.get(id=test_id).seconds if not None else -1
    context = {'test_seconds': seconds}
    return render_to_response('after_training.html', context)


def go_to_pairs(request):
    if request.session.get('state') == training_state:
        request.session['state'] = pairs_state
        return redirect('/pairs')
    else:
        return HttpResponseNotFound('Страница недоступна')


def pairs(request):
    check_image_pair_results(request)
    if request.session.get('state') != pairs_state:
        return HttpResponseNotFound('Страница недоступна')

    test_id = request.session.get('test_id')
    seconds = Test.objects.get(id=test_id).seconds if not None else -1
    image_pair_ids = request.session.get('image_pair_ids')

    ptr = request.session.get('image_pair_id_ptr') + 1
    if ptr > len(image_pair_ids) - 1:
        request.session['state'] = postquestions_state
        postquestions = PostQuestion.objects.filter(test=test_id).order_by('order')
        return question(request, next((q.id for q in postquestions if not q.isSeparator), None))

    request.session['image_pair_id_ptr'] = ptr
    image_pair = ImagePair.objects.get(id=image_pair_ids[ptr])
    left = '/media/' + str(image_pair.left.img)
    right = '/media/' + str(image_pair.right.img)

    context = {
        'image_pair_id': image_pair.id,
        'left': left,
        'right': right,
        'seconds': seconds,
        'is_training': False
    }
    return render_to_response('image_pair.html', context)


def final(request):
    check_question_results(request)
    request.session.modified = True
    test_id = request.session.get('test_id')
    test_ending = Test.objects.get(id=test_id).ending
    context = {'test_ending': test_ending}
    return render_to_response('final.html', context)


def failed(request):
    request.session.modified = True
    return render_to_response('final.html')


def results(request):
    if not request.user.is_superuser:
        return redirect('/admin')

    keys_times = {}

    cursor = connection.cursor()
    cursor.execute('''select distinct session_key_id, start_time from tests_userquestionresults''')
    key_time = cursor.fetchone()
    while key_time is not None:
        if key_time not in keys_times:
            keys_times[key_time] = {}
        uqrs = UserQuestionResults.objects.filter(session_key=key_time[0],
                                                  start_time=key_time[1]).order_by('id')
        for uqr in uqrs:
            uqr_question = uqr.question
            uqr_test = uqr.question.test
            uqr_answer = uqr.input_text if not None else uqr.answer.statement

            if uqr_test not in keys_times[key_time]:
                keys_times[key_time][uqr_test] = ([], [])
            keys_times[key_time][uqr_test][0].append((uqr_question, uqr_answer))

        key_time = cursor.fetchone()

    cursor.execute('''select distinct session_key_id, start_time from tests_userimagepairresults''')
    key_time = cursor.fetchone()
    while key_time is not None:
        if key_time not in keys_times:
            keys_times[key_time] = {}
        uips = UserImagePairResults.objects.filter(session_key=key_time[0],
                                                   start_time=key_time[1]).order_by('id')
        for uip in uips:
            uip_test = uip.pair.test
            left = uip.pair.left
            right = uip.pair.right
            if uip_test not in keys_times[key_time]:
                keys_times[key_time][uip_test] = ([], [])
            keys_times[key_time][uip_test][1].append(((left.img, left.name), (right.img, right.name),
                                                      2 if uip.choice else 1))
        key_time = cursor.fetchone()

    context = {
        'keys_times': keys_times
    }

    return render_to_response('results.html', context)


