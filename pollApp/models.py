from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class PollModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    is_ended = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.question} by {self.user.username}"
    
class PollOption(models.Model):
    poll = models.ForeignKey(PollModel, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.option_text} ({self.votes} votes)"
    
    
class UserVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(PollModel, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'poll')  

    def __str__(self):
        return f"{self.user.username} voted for '{self.option.option_text}' in '{self.poll.question}'"