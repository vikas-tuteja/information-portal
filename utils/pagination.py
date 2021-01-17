from rest_framework import pagination

class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 1000
