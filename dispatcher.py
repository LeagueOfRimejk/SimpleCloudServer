from request_parser import RequestParser

from views import http404_view


class ViewDispatcher:
    # Default Not Found View
    default_http_404 = http404_view
    request_parser = RequestParser()

    def __init__(self, url_patterns, route_resolver):
        self.url_patterns = url_patterns
        self.route_resolver = route_resolver

    def dispatch(self, request):
        # Transform Request to a Dictionary
        request_dict = self.request_parser.parse_request(request)

        # Extract path, and match pattern agains url_patterns
        path = request_dict["path"]
        match = self.route_resolver.match(path)
        if not match:
            return None
            
        view_func = match.view_func
        args = match.args
        kwargs = match.kwargs
        
        return view_func(request_dict, *args)