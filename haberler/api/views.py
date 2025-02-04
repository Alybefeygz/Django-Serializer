from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from haberler.models import Makale, Gazeteci
from haberler.api.serializers import MakaleSerilizer, GazeteciSerializer

#class view
from rest_framework.views import APIView


class GazeteciListCreateApiView(APIView):
    def get(self, request):
        yazarlar = Gazeteci.objects.all()
        serializer = GazeteciSerializer(yazarlar, many = True, context={'request': request})
        return Response(serializer.data)        
    
    def post(self, request):
        serializer = GazeteciSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MakaleListCreateApiView(APIView):
    def get(self, request):
        makaleler = Makale.objects.filter(aktif = True)
        serializer = MakaleSerilizer(makaleler, many = True)
        return Response(serializer.data)        
    
    def post(self, request):
        serializer = MakaleSerilizer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakaleDetailApiView(APIView):
    def get_object(self, pk):
        makale_instance = get_object_or_404(Makale, pk=pk)
        return makale_instance
    
    def get(self, request, pk):
        makale = self.get_object(pk=pk)
        serializer = MakaleSerilizer(makale)
        return Response(serializer.data)
        
    def put(self, request, pk):
        makale = self.get_object(pk=pk)
        serializer = MakaleSerilizer(makale, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        makale = self.get_object(pk=pk)
        makale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



############# FUNCTION METHOD #############

    
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def makale_detail_api_view(request, pk):
#     try:
#         makale_instance = Makale.objects.get(pk=pk)
#     except Makale.DoesNotExist:
#         return Response(
#             {
#                 'errors': {
#                     'code': 404,
#                     'message': f'Böyle bir id ({pk}) ile ilgili makale bulunamadı.'
#                 }
                    
#             }, 
#             status.HTTP_404_NOT_FOUND
#         )
#     if request.method == 'GET':
#         serializer = MakaleSerilizer(makale_instance)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         serializer = MakaleSerilizer(makale_instance, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'DELETE':
#         makale_instance.delete()
#         return Response(
#             {
#                 'islem': {
#                     'code': 204,
#                     'message': f' ({pk}) numaralı id silinmiştir.'
#                 }
                    
#             }, 
#             status.HTTP_204_NO_CONTENT
#         )


# @api_view(['GET', 'POST'])
# def makale_list_create_api_view(request):
    
#     if request.method == 'GET':
#         makaleler = Makale.objects.filter(aktif = True)
#         serializer = MakaleSerilizer(makaleler, many = True) #tek nesne değil query set??? many = True bu sorunu çözer
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = MakaleSerilizer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
    