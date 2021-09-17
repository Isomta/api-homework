from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets, mixins
from rest_framework.generics import CreateAPIView, ListAPIView

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import AdminOrReadOnly, IsOwnerOrReadOnly, \
    IsAdminOrReadOnly1
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer,
                          TitleAdminSerializer, TitleSerializer)


class CategoriesViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly1,]
    #filterset_class = CustomFilter
    search_fields = ['name']
    lookup_field = 'slug'


class GenresViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminOrReadOnly1, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
    #filterset_class = CustomFilter
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly1, ]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return TitleAdminSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs['title_id'],
            id=self.kwargs['review_id'],
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
