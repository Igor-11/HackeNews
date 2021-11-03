from django.contrib import admin
from .models import *
 
admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(Comment)

