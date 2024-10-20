from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *

class HotelViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    serializer_class = HotelSerializers
    queryset = Hotel.objects.all()

    def get_serializer_class(self):
        if self.action == 'upload_image':
            return HotelImageSerializers
        else:
            return self.serializer_class
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        hotel = self.get_object()
        serializers = self.get_serializer(
            hotel,
            data=request.data
        )

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
    #   self.queryset.filter(email = kwargs['email'])
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message' : 'hotel deleted successfully!'}, status.HTTP_200_OK)
