from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "exam"
        verbose_name_plural = "exams"

    def __str__(self):
        return self.title


class Question(models.Model):
    statement = models.TextField()
    score = models.IntegerField(default=1)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")

    class Meta:
        ordering = ["id"]
        verbose_name = "question"
        verbose_name_plural = "questions"

    def __str__(self):
        return self.statement[:50]


class Choice(models.Model):
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "choice"
        verbose_name_plural = "choices"

    def __str__(self):
        return self.text