from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (ListModelMixin,
                                   CreateModelMixin,
                                   RetrieveModelMixin,
                                   DestroyModelMixin,
                                   UpdateModelMixin)
from rest_framework.viewsets import ViewSetMixin
from rest_framework import serializers
from django.db.models.query import QuerySet
from django.db import models
from rest_framework.response import Response
from rest_framework import status


class QuerySetError(ValueError):
    pass


class SerializerClassError(ValueError):
    pass


class CustomGenericAPIView(GenericAPIView):
    queryset: QuerySet = None
    model: models.Model = None
    select: tuple[str] | str = None
    prefetch: tuple[str] | str = None

    def get_serializer_class(self):
        serializer = self.serializer_class
        if serializer:
            pass
        else:
            if self.request.method == "POST":
                serializer = self.create_serializer
            elif self.request.method == "GET":
                print(self.kwargs)
                model_fields = [field.name for field in self.get_model_fields()]
                if set(self.kwargs.keys()).intersection(set(model_fields)):
                    serializer = self.retrieve_serializer
                else:
                    serializer = self.list_serializer
            elif self.request.method in ["PUT", "PATCH"]:
                serializer = self.update_serializer

        assert serializer is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return serializer

    def get_queryset(self):
        queryset = self.queryset
        if queryset:
            pass
        else:
            if not self.model: raise QuerySetError('attribute model does not None')
            queryset = self.model.objects
            if self.select:
                queryset = queryset.select_related(*self.select) if isinstance(self.select, (
                    tuple, list)) else queryset.select_related(self.select)
            if self.prefetch:
                queryset = queryset.prefetch_related(*self.prefetch) if isinstance(self.prefetch, (
                    tuple, list)) else queryset.prefetch_related(self.prefetch)

        assert queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def get_model_fields(self):
        return self.model._meta.get_fields()


class CustomCreateModelMixin(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.model.objects.create(**serializer.primitive)

        for field in self.get_model_fields():
            if isinstance(field, models.ManyToManyField):
                data = serializer.validated_data.get(field.name, [])
                getattr(obj, field.name).set(data)

        self.perform_create(obj)
        headers = self.get_success_headers(serializer.data)
        return Response(self.list_serializer(obj).data, status=status.HTTP_201_CREATED, headers=headers)


class CustomUpdateModelMixin(UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        # partial = kwargs.pop('partial', False)
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        for k, v in serializer.primitive.items():
            setattr(obj, k, v)
        self.perform_update(obj)

        for field in serializer.collection:
            if isinstance(field, models.ManyToManyField):
                data = serializer.validated_data.get(field.name, [])
                getattr(obj, field.name).set(data)

        if getattr(obj, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            obj._prefetched_objects_cache = {}

        return Response(self.retrieve_serializer(obj).data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class CustomListAPIView(ListModelMixin,
                        CustomGenericAPIView):
    list_serializer: serializers.Serializer | serializers.ModelSerializer = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CustomListCreateAPIView(ListModelMixin,
                              CustomCreateModelMixin,
                              CustomGenericAPIView):
    list_serializer: serializers.Serializer | serializers.ModelSerializer = None
    create_serializer: serializers.Serializer | serializers.ModelSerializer = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomRetrieveUpdateDestroyAPIView(RetrieveModelMixin,
                                         CustomUpdateModelMixin,
                                         DestroyModelMixin,
                                         CustomGenericAPIView):
    retrieve_serializer: serializers.Serializer | serializers.ModelSerializer = None
    update_serializer: serializers.Serializer | serializers.ModelSerializer = None

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CustomModelViewSet(ViewSetMixin,
                         CustomListCreateAPIView,
                         CustomRetrieveUpdateDestroyAPIView):
    ...
