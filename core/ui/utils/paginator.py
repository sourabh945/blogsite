from django.core.paginator import Paginator , InvalidPage
from django.http import  Http404 , JsonResponse
from django.conf import settings
from urllib.parse import urlencode
from requests import request

class BasePagination:
    display_page_controls = False

    def paginate_queryset(self, queryset, request, view=None):  # pragma: no cover
        raise NotImplementedError('paginate_queryset() must be implemented.')

    def get_paginated_response(self, data):  # pragma: no cover
        raise NotImplementedError('get_paginated_response() must be implemented.')

    def get_paginated_response_schema(self, schema):
        return schema

    def to_html(self):  # pragma: no cover
        raise NotImplementedError('to_html() must be implemented to display page controls.')

    def get_results(self, data):
        return data['results']

    def get_schema_operation_parameters(self, view):
        return []


class BlogPaginator(BasePagination):
    """
        This is wrapper class for Pagintor class in django core, 
        it mimic the result as the rest_framework but it still works with 
        this simple django response function 
    """

    paginator_default = Paginator

    last_page_strings = ('last',)


    default_page_size = settings.DEFAULT_PAGE_SIZE
    max_page_size = settings.MAX_PAGE_SIZE

    def paginate_queryset(self, queryset,request:request):
        self.request = request 
        page_size = self.get_page_size()
        if not page_size:
            return None
        paginator:Paginator = self.paginator_default(queryset,page_size)
        page_number = self.get_page_number(request,paginator)
        try:
            self.page = paginator.page(page_number)
        except InvalidPage:
            return Http404(f'Page {page_number}is Not found')
        return list(self.page)

    def get_paginated_response(self,data):
        return JsonResponse({
            'count':self.page.paginator.count,
            'next':self.next_page_link(),
            'previous':self.previous_page_link(),
            'results':data
        },status=200)
        

    def get_page_size(self):
        size = self.request.GET.get('page_size',self.default_page_size)
        if size > self.max_page_size:
            size = self.max_page_size
        return int(size)
        
    def get_page_number(self,request,paginator):
        page_number = request.GET.get('page',1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        return page_number
    

    def next_page_link(self):
        if not self.page.has_next():
            return None
        parameters  = self.request.GET.copy()
        parameters['page'] = self.page.next_page_number()
        return f'{self.request.path}?{urlencode(parameters)}'

    def previous_page_link(self):
        if not self.page.has_previous():
            return None
        parameters = self.request.GET.copy()
        parameters['page'] = self.page.previous_page_number()
        return f'{self.request.path}?{urlencode(parameters)}'
    
    