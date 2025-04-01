from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer
from .pagination import CustomPagination
from usuarios.permissions import EsPropietario  # Importa tu permiso personalizado

class ProductoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.filter(activo=True).select_related('categoria', 'vendedor')
    serializer_class = ProductoSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    filterset_fields = {
        'categoria': ['exact'],
        'precio': ['gte', 'lte'],
        'activo': ['exact'],
        'vendedor': ['exact'],  # Nuevo filtro por vendedor
        'destacado': ['exact']
    }
    search_fields = ['nombre', 'descripcion', 'categoria__nombre', 'vendedor__email']
    ordering_fields = ['precio', 'nombre', 'fecha_creacion', 'vendedor__email']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro especial para /mis-productos/
        if self.request.path.endswith('/mis-productos/'):
            return queryset.filter(vendedor=self.request.user)
            
        return queryset

    def perform_create(self, serializer):
        imagen = self.request.FILES.get('imagen')
        instance = serializer.save(vendedor=self.request.user)
        
        if imagen:
            instance.imagen = imagen
            instance.save()

class ProductoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all().select_related('categoria', 'vendedor')
    serializer_class = ProductoSerializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticatedOrReadOnly, EsPropietario]

    def perform_update(self, serializer):
        imagen = self.request.FILES.get('imagen')
        instance = serializer.save()
        
        # No permitir cambiar el vendedor
        if 'vendedor' in serializer.validated_data:
            instance.vendedor = self.request.user
            instance.save()
        
        if imagen:
            instance.imagen = imagen
            instance.save()

    def perform_destroy(self, instance):
        instance.activo = False
        instance.save()

class MisProductosListAPIView(generics.ListAPIView):
    serializer_class = ProductoSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Producto.objects.filter(
            vendedor=self.request.user
        ).select_related('categoria')

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def categoria_list(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def categoria_detail(request, pk):
    try:
        categoria = Categoria.objects.get(pk=pk)
    except Categoria.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)