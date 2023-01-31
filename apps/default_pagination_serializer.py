from rest_framework.pagination import PageNumberPagination


class DefaultPaginationSerializer(PageNumberPagination):
    page_size = 100
    max_page_size = 200
