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

    class Meta:
        unique_together = (('test','order'),)

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
    img = models.ImageField(upload_to='img/')
    test = models.ForeignKey(Test)

    def __str__(self):
        return self.name


class ImagePair(models.Model):
    test = models.ForeignKey(Test)
    left = models.ForeignKey(Image, related_name='%(class)s_left')
    right = models.ForeignKey(Image, related_name='%(class)s_right')

    def __str__(self):
        #return 'pair(%s,%s)' % str(self.left), str(self.right)
        return 'pair'