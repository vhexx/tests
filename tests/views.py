from django.shortcuts import render_to_response


def test(request):
    return render_to_response('test.html')


def question(request):
    return render_to_response('question.html')