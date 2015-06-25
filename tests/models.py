from django.db import models


class Test(models.Model):
    title = models.CharField(max_length=100)
    seconds = models.IntegerField(null=True, blank=True)

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
    func = models.CharField(max_length=100)
    test = models.ForeignKey(Test)

    def __str__(self):
        return self.func


class Image(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField()
    test = models.ForeignKey(Test)


class ImagePair(models.Model):
    test = models.ForeignKey(Test)
    left = models.ForeignKey(Image)
    right = models.ForeignKey(Image)


# ########################################################
# ########################################################
# ########################################################
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
            return ('answer:' + str(self.statement))
        elif self.statement is not None:
            return ('img:' + str(self.image))
        else:
            return ('Empty')

