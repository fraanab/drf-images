from django.contrib import admin

from .models import Comment, Membership, Task, Team

admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Membership)
admin.site.register(Team)
