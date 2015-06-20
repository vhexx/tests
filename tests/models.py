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
        return (str(self.ref))


class AnswerPrototype(models.Model):
    question = models.ForeignKey(QuestionPrototype)
    statement = models.CharField(max_length=300, null=True, blank=True)
    image = models.ForeignKey(ImagePrototype, null=True, blank=True)

    def __str__(self):
        if self.statement is not None and len(self.statement) > 0:
            return ('answer:'+str(self.statement))
        elif self.statement is not None:
            return ('img:' + str(self.image))
        else:
            return ('Empty')