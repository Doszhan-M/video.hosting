from elasticsearch_dsl import Q

from rest_framework import status
from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    DestroyAPIView, UpdateAPIView, GenericAPIView,
)

from .documents import VideoDocument
from .serializers import (
    VideoSerializer, UpdateCreateVideoSerializer,
    CreateCommentSerializer, CommentSerializer,)
from .models import Video, Comment, SubscribeChannel

from django.conf import settings
from django.contrib.auth import get_user_model
from importlib import import_module  

class SearchVideo(ListAPIView):
    ''' Search video
    '''
    serializer_class = VideoSerializer

    def get_queryset(self, *args, **kwargs):
        session_data = 'mve308h4dxoi4k5m7pu625jj7n0y4t93'
        django_session_engine = import_module(settings.SESSION_ENGINE)
        session = django_session_engine.SessionStore(session_data)
        uid = session.get('_auth_user_id')
        user = get_user_model().objects.get(id=uid)
        print(user)
        
        value = self.kwargs['query']
        query = Q('multi_match', query=value,
                  fields=[
                      'title',
                      'description',
                      'hashtag',
                  ], fuzziness='auto')
        search = VideoDocument.search().query(query)
        queryset = search.to_queryset()
        return queryset


class All_Videos(ListAPIView):
    ''' Get all video
    '''
    queryset = Video.objects.all().order_by('-upload_date')
    serializer_class = VideoSerializer


class GetVideo(RetrieveAPIView):
    ''' Get video by id
    '''
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class CreateVideo(CreateAPIView):
    ''' Create video
    '''
    queryset = Video.objects.all()
    serializer_class = UpdateCreateVideoSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(
            channel=self.request.user.user_channel)


class DeleteVideo(DestroyAPIView):
    ''' Delete video
    '''
    queryset = Video.objects.all()
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.user_channel == instance.channel:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class UpdateVideo(UpdateAPIView):
    ''' Update video
    '''
    queryset = Video.objects.all()
    serializer_class = UpdateCreateVideoSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.user_channel == instance.channel:
            return self.update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)


class LikeVideo(GenericAPIView):
    ''' Like video
    '''
    queryset = Video.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        instance = self.get_object()
        instance.likes.add(request.user)
        return Response(status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            return VideoSerializer
        return super().get_serializer_class()


class CreateComment(CreateAPIView):
    ''' Create comment for video
    '''
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VideoComments(ListAPIView):
    ''' Get all comments for video
    '''
    serializer_class = CommentSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()
        queryset = Comment.objects.filter(
            video=self.kwargs['pk']).order_by('-create')
        return queryset


class SubscribeVideoChannel(GenericAPIView):
    ''' Subscribe to video's channel
    '''
    queryset = Video.objects.all()
    serializer_class = None
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        video = self.get_object()
        SubscribeChannel.objects.create(channel=video.channel,
                                        user=request.user)
        return Response(status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            return VideoSerializer
        return super().get_serializer_class()
    

class SubscribedVideos(ListAPIView):
    ''' Get all videos from subscribes
    '''
    serializer_class = VideoSerializer

    def get_queryset(self):
        queryset = QuerySet(Video)
        subscribes = SubscribeChannel.objects.filter(user=self.request.user)
        for subscribe in subscribes:
            channel = subscribe.channel
            channel_videos = Video.objects.filter(channel=channel)
            queryset.union(channel_videos)
        return queryset
