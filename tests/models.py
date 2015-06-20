from django.db import models


class TestPrototype(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return (self.title)


class QuestionPrototype(models.Model):
    title = models.CharField(max_length=200)
    test = models.ForeignKey(TestPrototype)

    def __str__(self):
        return (self.title)


class ImagePrototype(models.Model):
    ref = models.CharField(max_length=200)

    def __str__(self):
        return ('img:' + str(self.ref))


class AnswerPrototype(models.Model):
    question = models.ForeignKey(QuestionPrototype)
    statement = models.CharField(max_length=300, null=True)
    image = models.ForeignKey(ImagePrototype, null=True)

    def __str__(self):
        if self.statement is not None:
            return ('Answer:'+str(self.statement))
        elif self.statement is not None:
            return ('img:' + str(self.image))
        else
            return ('Empty')