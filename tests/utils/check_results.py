from tests.models import UserQuestionResults, Question


def check_results(request):
    session_key = request.session.session_key
    questions = dict(request.GET)
    cached_questions = {}
    for q in questions:
        if q not in cached_questions:
            if q.isdigit():
                cached_questions[q] = Question.objects.get(id=int(q))
            else:
                return False
        for a in questions[q]:
            # TODO check question type and answer
            if a.isdigit():
                uqr = UserQuestionResults(
                    UserQuestionResults.objects.latest(
                        'id').id + 1 if UserQuestionResults.objects.count() > 0 else 1,
                    session_key,
                    int(q),
                    int(a),
                    None
                )
            else:
                uqr = UserQuestionResults(
                    UserQuestionResults.objects.latest('id').id + 1,
                    session_key,
                    int(q),
                    None,
                    a
                )
            uqr.save()