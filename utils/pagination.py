from rest_framework import pagination

class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 1000


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
