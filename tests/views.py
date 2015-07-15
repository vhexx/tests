from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.db import connection
import time
from tests.models import PreQuestion, Test, Answer, PostQuestion, ImagePair, TrainingImagePair, Question, \
    UserQuestionResults, UserImagePairResults
from .const import prequestions_state, postquestions_state, pairs_state, training_state, initial_state
from tests.utils.check_results import check_question_results, check_image_pair_results
from tests.utils.prepare_images import prepare_images
from tests.utils.serialize import serialize_image_pair_ids, deserialize_image_pair_ids


def index(requst):
    return redirect('/admin')


def test(request, test_id):
    if test_id is None:
        test_id = request.session.get('test_id')
        if test_id is not None:
            return redirect('/test/' + str(test_id))
        else:
            return page_unavailable(request, 'Страница недоступна')

    try:
        test_instance = Test.objects.get(id=test_id)

    except Exception:
        return page_unavailable(request, 'Запрашиваемый тест не найден')

    # put current test id in session
    request.session['start_time'] = int(time.time())
    request.session['test_id'] = test_id
    request.session['state'] = prequestions_state

    # set expiration time - one month
    request.session.set_expiry(2592000)

    # retrieve image pairs, shuffle them and put in session
    image_pair_ids = prepare_images(test_id)
    request.session['image_pair_ids'] = serialize_image_pair_ids(image_pair_ids)
    request.session['image_pair_id_ptr'] = -1

    # retrieve related questions and put them in session
    prequestions = PreQuestion.objects.filter(test=test_id).order_by('order')

    context = {
        'test_title': test_instance.title,
        'question_id': next((q.id for q in prequestions if not q.isSeparator), None),
        'test_description': test_instance.description
    }
    return render_to_response('test.html', context)


def question(request, question_id):
    state = request.session.get('state')
    if state is None or state not in (prequestions_state, postquestions_state):
        return page_unavailable(request, 'Страница недоступна')

    if check_question_results(request):
        return final(request, True)
    question_id = int(question_id)

    test_id = request.session.get('test_id')
    if test_id is None:
        return page_unavailable(request, 'Страница недоступна')

    if request.session.get('state') == prequestions_state:
        model = PreQuestion
    elif request.session.get('state') == postquestions_state:
        model = PostQuestion
    else:
        return page_unavailable(request, 'Страница недоступна')

    questions = model.objects.filter(test=test_id).order_by('order')

    if len(questions) == 0:
        return page_unavailable(request, 'Страница недоступна')

    if question_id not in list(map(lambda q: q.id, questions)):
        return page_unavailable(request, 'Страница недоступна')

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

    if first_found != 1:
        return page_unavailable(request, 'Произошла ошибка')

    questions_and_answers = []

    for q in actual_questions:
        questions_and_answers.append((q, Answer.objects.filter(question=q.id)))

    cursor = connection.cursor()
    cursor.execute('''select count(*)
                        from (select question_id
                                from tests_userquestionresults
                                group by question_id, session_key, start_time
                                having session_key=%s
                                and start_time=%s) as q''',
                   [request.session.session_key, int(request.session.get('start_time'))])
    question_passed = cursor.fetchone()[0]

    try:
        question_instance = model.objects.get(id=question_id)
    except Exception:
        return page_unavailable(request, 'Произошла ошибка')

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
    state = request.session.get('state')
    if state is None or state != prequestions_state:
        return page_unavailable(request, 'Страница недоступна')

    if check_question_results(request):
        return final(request, True)

    request.session['state'] = training_state
    training_image_pairs = TrainingImagePair.objects.all().order_by('id')
    context = {
        'training_image_pair_id': training_image_pairs[0].id if len(training_image_pairs) > 0 else 0
    }
    return render_to_response('before_training.html', context)


def training(request, training_image_pair_id):
    if request.session.get('state') != training_state:
        return before_training(request)

    training_image_pair_id = int(training_image_pair_id)

    test_id = request.session.get('test_id')

    if test_id is not None:
        try:
            test_instance = Test.objects.get(id=test_id)
            seconds = test_instance.seconds if test_instance.seconds is not None else ''
        except Exception:
            return page_unavailable(request, 'Произошла ошибка')
    else:
        return page_unavailable(request, 'Страница недоступна')

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
    return after_training(request)


def after_training(request):
    test_id = request.session.get('test_id')
    if test_id is not None:
        try:
            test_instance = Test.objects.get(id=test_id)
            seconds = test_instance.seconds if test_instance.seconds is not None else ''
        except Exception:
            return page_unavailable(request, 'Произошла ошибка')

    state = request.session.get('state')
    if state is None or state != prequestions_state:
        return page_unavailable(request, 'Страница недоступна')

    if check_question_results(request):
        return final(request, True)

    request.session['state'] = training_state
    
    context = {
        'test_seconds': seconds
    }
    return render_to_response('after_training.html', context)


def go_to_pairs(request):
    test_id = request.session.get('test_id')

    if test_id is not None:
        if request.session.get('state') == training_state:
            request.session['state'] = pairs_state
            return redirect('/pairs')
        else:
            return after_training(request)
    else:
        return page_unavailable(request, 'Страница недоступна')


def pairs(request):
    check_image_pair_results(request)
    test_id = request.session.get('test_id')

    if test_id is not None:
        if request.session.get('state') != pairs_state:
            return after_training(request, test_id)
        try:
            test_instance = Test.objects.get(id=test_id)
            seconds = test_instance.seconds if test_instance.seconds is not None else ''
        except Exception:
            page_unavailable(request, 'Произошла ошибка')
    else:
        return page_unavailable(request, 'Страница недоступна')

    image_pair_ids_string = str(request.session.get('image_pair_ids'))
    image_pair_ids = deserialize_image_pair_ids(image_pair_ids_string)

    ptr = int(request.session.get('image_pair_id_ptr')) + 1
    if ptr > len(image_pair_ids) - 1:
        request.session['state'] = postquestions_state
        postquestions = PostQuestion.objects.filter(test=test_id).order_by('order')
        return question(request, next((q.id for q in postquestions if not q.isSeparator), None))

    request.session['image_pair_id_ptr'] = ptr
    try:
        image_pair = ImagePair.objects.get(id=int(image_pair_ids[ptr]))
    except Exception:
        return page_unavailable(request, 'Произошла ошибка')

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


def final(request, isFailed=False):
    if isFailed is None or isFailed is not True:
        check_question_results(request)

    test_id = request.session.get('test_id')
    if test_id is None:
        return page_unavailable(request, 'Страница недоступна')
    try:
        test_instance = Test.objects.get(id=test_id)
        test_ending = test_instance.ending if test_instance.ending is not None else ''
    except Exception:
        return page_unavailable(request, 'Произошла ошибка')

    request.session['test_id'] = None
    request.session['state'] = initial_state

    context = {
        'test_ending': test_ending
    }
    return render_to_response('final.html', context)


def results1(request):
    if not request.user.is_superuser:
        return redirect('/admin')

    keys_times = {}

    cursor = connection.cursor()
    cursor.execute('''select distinct session_key, start_time
                        from tests_userquestionresults
                        order by start_time desc''')
    key_time = cursor.fetchone()
    while key_time is not None:
        if key_time not in keys_times:
            keys_times[key_time] = {}
        uqrs = UserQuestionResults.objects.filter(session_key=key_time[0],
                                                  start_time=key_time[1]).order_by('id')
        for uqr in uqrs:
            uqr_question = uqr.question
            uqr_test = uqr.question.test
            try:
                uqr_answer = uqr.input_text if uqr.input_text is not None else uqr.answer.statement
            except Exception:
                uqr_answer = ''

            #Todo view of session key
            if uqr_test not in keys_times[key_time]:
                keys_times[key_time][uqr_test] = ([], [])
            keys_times[key_time][uqr_test][0].append((uqr_question, uqr_answer))

        key_time = cursor.fetchone()

    cursor.execute('''select distinct session_key, start_time
                        from tests_userimagepairresults
                        order by start_time desc''')
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

            keys_times[key_time][uip_test][1].append(
                '<a {0} href="{1}">{2}</a><br/><a {3} href="{4}">{5}</a><br/><br/>'.format(
                    '' if uip.choice else 'style="font-weight: bold;"',
                    '/media/' + str(left.img),
                    str(left.name),
                    'style="font-weight: bold;"' if uip.choice else '',
                    '/media/' + str(right.img),
                    str(right.name)
                )
            )
        key_time = cursor.fetchone()

    time_res = list(keys_times.items())
    time_res.sort(key=lambda i: i[0][1], reverse=True)
    time_res = list(map(lambda i: ((i[0][0], time.strftime("%b %d %Y %H:%M", time.gmtime(i[0][1]))), i[1]), time_res))

    context = {
        'time_res': time_res
    }
    return render_to_response('results.html', context)


def results(request):
    if not request.user.is_superuser:
        return redirect('/admin')

    keys_times = {}

    cursor = connection.cursor()
    cursor.execute('''select distinct session_key, start_time
                        from tests_userquestionresults
                        order by start_time desc''')
    key_time = cursor.fetchone()
    while key_time is not None:
        uqrs = UserQuestionResults.objects.filter(session_key=key_time[0], start_time=key_time[1])
        test_instance = uqrs.get().question.test
        test_questions = Question.objects.filter(test=test_instance).order_by('order')
        qa = {}
        for q in test_questions:
            answers_string = ''
            question_uqrs = uqrs.filter(question=q)
            for r in question_uqrs:
                answers_string = answers_string+r.answer.statement+', '
            qa[q.title] = answers_string

        uirs = UserImagePairResults.objects.filter(session_key=key_time[0], start_time=key_time[1])
        test_imagepairs = ImagePair.objects.filter(test=test_instance)
        ic = {}
        for i in test_imagepairs:
            choices_string=''
            imagepair_uirs = uirs.filter(pair=i).order_by('id')
            for r in imagepair_uirs:
                choices_string = choices_string+str(r.choice)
            ic[str(i.left.img.url)+' or '+str(i.right.img.url)] = choices_string

        keys_times[str(key_time[0])+str(key_time[1])] = (qa, ic)

        key_time = cursor.fetchone()

    context = {'keytimes' : keys_times}
    return render_to_response('results.html', context)


def page_unavailable(request, message):
    return render_to_response('unavailable.html', {'message': message})