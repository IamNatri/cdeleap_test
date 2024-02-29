from rest_framework import viewsets, status
from rest_framework.response import Response
from careers.api import serializer
from careers import models


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.PostSerializer
    queryset = models.Post.objects.all()
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        required_fields = ['username', 'title', 'content']
        data = request.data

        for field in required_fields:
            if field not in data:
                return Response({"detail": f"Field '{field}' is a required field."},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(super().create(request, *args, **kwargs).data,
                        status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        # specify the fields allowed to be updated
        allowed_fields = ['title', 'content']

        # check if any of the fields in the request are not allowed
        for field in data.keys():
            if field not in allowed_fields:
                return Response({"detail": f"Field '{field}' not allowed to be updated."},
                                status=status.HTTP_400_BAD_REQUEST)

        for field in allowed_fields:
            if field in data:
                setattr(instance, field, data[field])

        instance.save()
        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)
