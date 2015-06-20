from django.shortcuts import render_to_response


def test(request):
    render_to_response('test.html')


def question(request):
    render_to_response('question.html')