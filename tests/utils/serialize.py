# gets question QuerySet and returns serialized string
def serialize_questions(question_set):
    question_string = ''
    for q in question_set:
        question_string = question_string + str(q.id) + ';'
    return question_string[:-1]

# gets serialized string and resturns list of ids(int)
def deserialize_questions(question_string):
    return list(map(int, question_string.split(';')))

