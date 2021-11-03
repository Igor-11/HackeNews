from django.db import models

from django.db import models
from django.contrib.auth.models import User

 
class Post(models.Model):
    title = models.CharField("HeadLine", max_length=256, unique=True)
    link = models.URLField("LINK", max_length=256,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    amount_of_upvotes = models.IntegerField(null=True)
    author_name = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    description = models.TextField("Description", blank=True)
    comments = models.IntegerField(null=True)    
 
    def __unicode__(self):
        return self.title
 
    def count_votes(self):
        self.amount_of_upvotes = Vote.objects.filter(post = self).count()
     
    def count_comments(self):
        self.comments = Comment.objects.filter(post = self).count()
 
 
 
class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
 
    def __unicode__(self):
        return f"{self.user.username} upvoted {self.link.title}"
 
 
class Comment(models.Model):
    author_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    identifier = models.IntegerField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
 
    def __unicode__(self):
        return f"Comment by {self.user.username}"
