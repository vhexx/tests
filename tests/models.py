from django.db import models


class TestPrototype:
    title = models.CharField(max_length=100)


class QuestionPrototype:
    title = models.CharField(max_length=200)
    test = models.ForeignKey(TestPrototype)


class AnswerPrototype:
    question = models.ForeignKey(QuestionPrototype)
    statement = models.CharField(max_length=300, null=True)
    image = models.ForeignKey(ImagePrototype, null=True)


class ImagePrototype:
    img = models.ImageField()