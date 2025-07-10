from rest_framework.pagination import PageNumberPagination


class MyUserPagination(PageNumberPagination):
    page_size_query_param = 'limit'
