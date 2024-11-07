from django.db import models
from django.utils import timezone

# Fanlar (Subject)
class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Mavzular (Topic)
class Topic(models.Model):
    subject = models.ForeignKey(Subject, related_name='topics', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    view_deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

# Savollar (Question)
class Question(models.Model):
    topic = models.ForeignKey(Topic, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    start_time = models.DateTimeField(blank=True, null=True)  # Savol boshlanish vaqti
    end_time = models.DateTimeField(blank=True, null=True)    # Savol tugash vaqti
    is_repeatable = models.BooleanField(default=False)

    # def is_available(self):
    #     now = timezone.now()
    #     if self.start_time and self.end_time:
    #         return self.start_time <= now <= self.end_time
    #     return True  # Agar vaqt cheklovi bo'lmasa, savol har doim ochiq bo'ladi


    def __str__(self):
        return self.text
