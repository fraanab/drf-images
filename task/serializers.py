from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comment, Membership, Task, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    teamname = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ['content', 'thumbnail', 'thumbnail_url', 'created_at', 'completed', 'id', 'username', 'team', 'teamname']

    def get_teamname(self, obj):
        if obj.team:
            return obj.team.teamname
        return None
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        return None
            
class MembershipSerializer(serializers.ModelSerializer):
    teamname = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = ['team', 'member', 'teamname']

    def get_teamname(self, obj):
        return obj.team.teamname
