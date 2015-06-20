from django.db import models


class TestPrototype(models.Model):
    title = models.CharField(max_length=100)


class QuestionPrototype(models.Model):
    title = models.CharField(max_length=200)
    test = models.ForeignKey(TestPrototype)


class AnswerPrototype(models.Model):
    question = models.ForeignKey(QuestionPrototype)
    statement = models.CharField(max_length=300, null=True)
    image = models.ForeignKey(ImagePrototype, null=True)


class ImagePrototype(models.Model):
    img = models.ImageField()