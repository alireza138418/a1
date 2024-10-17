from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .serializers import *

class HotelViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    serializer_class = HotelSerializers
    queryset = Hotel.objects.all()

    def destroy(self, request, *args, **kwargs):
    #   self.queryset.filter(email = kwargs['email'])
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message' : 'hotel deleted successfully!'}, status.HTTP_200_OK)
