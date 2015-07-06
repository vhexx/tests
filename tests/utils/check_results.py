def check_results(request):
    params = dict(request.GET)
    for i in params:
        print(i, params[i])