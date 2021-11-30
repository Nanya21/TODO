from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth import get_user_model
# Create your models here.

User=get_user_model()
class Todo(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name='todo')
    title=models.CharField(max_length=200)
    body= models.TextField()
    completed=models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self)-> str:
        return f'{self.activity} for {self.user.username}'

    def delete(self):
        self.is_active = False
        self.save()
        return

