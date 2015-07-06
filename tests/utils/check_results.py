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
                    id=UserQuestionResults.objects.latest('id').id + 1,
                    session_key=session_key,
                    question=int(q),
                    answer=int(a)
                )
            else:
                uqr = UserQuestionResults(
                    id=UserQuestionResults.objects.latest('id').id + 1,
                    session_key=session_key,
                    question=int(q),
                    input_text=a
                )
            uqr.save()