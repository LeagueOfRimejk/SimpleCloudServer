from route import RouteResolver

from dispatcher import ViewDispatcher

from url_patterns import url_patterns

class Application:
    # Main Components
    route_resolver = RouteResolver(url_patterns)
    dispatcher = ViewDispatcher(url_patterns, route_resolver)

    def handle_request(self, request):
        response = self.dispatcher.dispatch(request)
        # If there was no response, that means that request for
        # particular URL not match any of the declared patterns, hence
        # return default HTTP 404
        if not response:
            response = self.dispatcher.default_http_404()
            return response()
        
        return response()