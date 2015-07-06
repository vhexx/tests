from django.contrib.sessions.models import Session
from django.db import models


class Test(models.Model):
    title = models.CharField(max_length=100)
    seconds = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class QuestionType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Question(models.Model):
    title = models.CharField(max_length=200)
    order = models.IntegerField()
    test = models.ForeignKey(Test)
    type = models.ForeignKey(QuestionType)
    isSeparator = models.BooleanField(default=False)

    class Meta:
        unique_together = (('test', 'order'),)

    def __str__(self):
        return self.title


class PreQuestion(Question):
    pass


class PostQuestion(Question):
    pass


class Answer(models.Model):
    statement = models.CharField(max_length=300, null=True, blank=True)
    question = models.ForeignKey(Question)

    def __str__(self):
        return self.statement


class FailureCriterion(models.Model):
    test = models.ForeignKey(Test)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)

    def __str__(self):
        return 'Failure criterion'


class FCFunction(models.Model):
    test = models.ForeignKey(Test)
    func = models.CharField(max_length=100)

    def __str__(self):
        return self.func


class Image(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='img/')
    test = models.ForeignKey(Test)

    def __str__(self):
        return self.name


class ImagePair(models.Model):
    test = models.ForeignKey(Test)
    left = models.ForeignKey(Image, related_name='%(class)s_left')
    right = models.ForeignKey(Image, related_name='%(class)s_right')
    repeats = models.IntegerField(default=1)

    def __str__(self):
        return 'pair'


class TrainingImagePair(models.Model):
    text = models.CharField(max_length=300, null=True, blank=True)
    left = models.ImageField(upload_to='img/')
    right = models.ImageField(upload_to='img/')


class UserQuestionResults(models.Model):
    session_key = models.ForeignKey(Session)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer, null=True, blank=True)
    input_text = models.CharField(null=True, blank=True)


class UserImagePairResults(models.Model):
    session_key = models.ForeignKey(Session)
    pair = models.ForeignKey(ImagePair)
    choice = models.BooleanField()

