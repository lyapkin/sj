from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


from .models import Cart
from .serializers import CartSerializer


class CartApi(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Cart.objects.all().order_by('-id')
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            self.kwargs['pk'] = request.data['id']
            response = self.update(request, partial=True, *args, **kwargs)
        except Http404:
            print('create')
            data = {
                'product': request.data['id'],
                'user': request.user.id,
                'quantity': request.data['quantity'] 
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            data = self.get_queryset().filter(user=data['user'])
            response_serializer = self.get_serializer(data, many=True)
            response = Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return response
    
    def update(self, request, *args, **kwargs):
        response =  super().update(request, *args, **kwargs)
        data = self.get_queryset().filter(user=request.user.id)
        response_serializer = self.get_serializer(data, many=True)
        response.data = response_serializer.data
        return response
    
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = self.get_serializer(self.get_queryset().filter(user=request.user.id), many=True).data
        return response
    
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter_kwargs = {'user': self.request.user.id, 'product': self.kwargs['pk']}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
    
    @action(detail=False, methods=['delete'])
    def clean(self, request):
        self.get_queryset().filter(user=request.user.id).delete()
        data = self.get_queryset().filter(user=request.user.id)
        return Response(self.get_serializer(data, many=True).data, status=status.HTTP_204_NO_CONTENT)

    # def get_queryset(self):
    #     return super().get_queryset().translated()