from .filters import CustomFilter
from .models import Category, Genre, Title
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from .permissions import AdminOrReadOnly
from .serializers import (
    GenresSerializer, CategoriesSerializer, TitleSerializer,TitleAdminSerializer)

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .models import Review
from .serializers import (CommentSerializer, ReviewSerializer)
from .permissions import IsOwnerOrReadOnly



class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (AdminOrReadOnly,)
    search_fields = ['name',]
    lookup_field = 'slug'


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name',]
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminOrReadOnly,)
    filterset_class = CustomFilter

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
