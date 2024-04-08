from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from nest.models import Property
from .serializers import PropertySerializer, PropertyMinimalSerializer
from django.http import Http404
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


# Create your views here.
class PropertyListAPIView(APIView):
    def get(self, request):
        properties = Property.objects.all().order_by("id")
        pagination = CustomPagination()
        paginated_properties = pagination.paginate_queryset(properties, request)
        serializer = PropertyMinimalSerializer(paginated_properties, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        property = self.get_object(pk)
        serializer = PropertySerializer(property)
        return Response(serializer.data)

    def put(self, request, pk):
        property = self.get_object(pk)
        serializer = PropertySerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        property = self.get_object(pk)
        property.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
