from django.shortcuts import redirect
from tests.const import prequestions_state
from tests.models import UserQuestionResults, Question, UserImagePairResults, FCFunction, FailureCriterion
from tests.views import failed


def check_question_results(request):
    session_key = request.session.session_key
    start_time = request.session.get('start_time')
    questions = dict(request.GET)
    cached_questions = {}
    for q in questions:
        if q not in cached_questions:
            if q.isdigit():
                q_id = int(q)
                cached_questions[q] = Question.objects.get(id=q_id)
                UserQuestionResults.objects.filter(session_key=session_key, start_time=start_time,
                                                   question=q_id).delete()
            else:
                return False
        for a in questions[q]:
            # TODO check question type and answer
            id = UserQuestionResults.objects.latest('id').id + 1 if UserQuestionResults.objects.count() > 0 else 1
            if a.isdigit():
                uqr = UserQuestionResults(
                    id,
                    session_key,
                    start_time,
                    int(q),
                    int(a),
                    None
                )
            else:
                uqr = UserQuestionResults(
                    id,
                    session_key,
                    start_time,
                    int(q),
                    None,
                    a
                )
            uqr.save()

    # check criterion
    if request.session.get('state') == prequestions_state:
        test_id = request.session.get('test_id')
        fc_function = FCFunction.objects.filter(test=test_id)
        if len(fc_function) == 0:
            return
        fc_function = fc_function[0].func
        fcs = FailureCriterion.objects.filter(test=test_id).order_by('id')
        index = 0
        for fc in fcs:
            index += 1
            value = 1 if len(UserQuestionResults.objects.filter(session_key=session_key, start_time=start_time,
                                                                question=fc.question.id,
                                                                answer=fc.answer.id)) > 0 else 0
            fc_function = fc_function.replace('{' + str(index) + '}', str(value))

        result = 0
        try:
            result = eval(fc_function)
        except Exception:
            pass

        if result == 1:
            return failed(request)


def check_image_pair_results(request):
    session_key = request.session.session_key
    start_time = request.session.get('start_time')
    params = dict(request.GET)
    pair = params.get('pair')
    choice = params.get('choice')
    if pair is None or choice is None:
        return
    if len(pair) == 0 and len(choice) == 0:
        return

    pair = pair[0]
    choice = choice[0]

    if not pair.isdigit() or not choice.isdigit():
        return False

    id = UserImagePairResults.objects.latest('id').id + 1 if UserImagePairResults.objects.count() > 0 else 1
    uipr = UserImagePairResults(
        id,
        session_key,
        start_time,
        int(pair),
        int(choice)
    )
    uipr.save()
