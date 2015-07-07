from tests.models import UserQuestionResults, Question, UserImagePairResults


def check_question_results(request):
    session_key = request.session.session_key
    questions = dict(request.GET)
    cached_questions = {}
    for q in questions:
        if q not in cached_questions:
            if q.isdigit():
                q_id = int(q)
                cached_questions[q] = Question.objects.get(id=q_id)
                UserQuestionResults.objects.filter(session_key=session_key, question=q_id).delete()
            else:
                return False
        for a in questions[q]:
            # TODO check question type and answer
            id = UserQuestionResults.objects.latest('id').id + 1 if UserQuestionResults.objects.count() > 0 else 1
            if a.isdigit():
                uqr = UserQuestionResults(
                    id,
                    session_key,
                    int(q),
                    int(a),
                    None
                )
            else:
                uqr = UserQuestionResults(
                    id,
                    session_key,
                    int(q),
                    None,
                    a
                )
            uqr.save()


def check_image_pair_results(request):
    session_key = request.session.session_key
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

    id = UserImagePairResults.objects.latest('id').id + 1 if UserQuestionResults.objects.count() > 0 else 1
    uipr = UserImagePairResults(
        id,
        session_key,
        int(pair),
        int(choice)
    )
    uipr.save()
