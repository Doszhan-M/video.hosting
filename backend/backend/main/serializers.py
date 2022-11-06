from os.path import splitext

from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    ModelSerializer, FileField, PrimaryKeyRelatedField,
    CharField, SerializerMethodField)

from .models import Video, Channel, Comment


class VideoSerializer(ModelSerializer):

    video_file = FileField(required=False)
    channel = PrimaryKeyRelatedField(queryset=Channel.objects.all(), required=False)
    username = CharField(source="channel.owner.first_name", read_only=True)
    user_avatar = CharField(source="channel.owner.avatar.url")
    
    class Meta:
        model = Video
        fields = (
            'id', 'channel', 'title', 'description',
            'video_file', 'hashtag', 'upload_date', 'likes',
            'username', 'user_avatar')
        

class UpdateCreateVideoSerializer(ModelSerializer):

    video_file = FileField(required=False)

    class Meta:
        model = Video
        fields = (
            'title', 'description', 'video_file',
            'hashtag', 'upload_date', 'likes')

    def validate_video_file(self, value):
        file_extension = splitext(value.name)[-1].lower()
        extensions = ['.mov', '.avi', '.mp4', '.webm', '.mkv']
        if file_extension not in extensions:
            raise ValidationError
        return value
    
class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text', 'user', 'create')


class CreateCommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text', 'video',)
