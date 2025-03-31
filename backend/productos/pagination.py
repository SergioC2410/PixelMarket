# productos/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10  # Tamaño de página por defecto
    page_size_query_param = 'page_size'  # Parámetro para cambiar el tamaño
    max_page_size = 100  # Tamaño máximo permitido

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data,
            'total_items': self.page.paginator.count,
        })