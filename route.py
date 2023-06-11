import re


from regex_resolver import URLRegexResolver

class RoutePattern:
    # Default URL resolver
    url_resolver = URLRegexResolver()

    # List that holds corresponding View function to url_pattern
    views = list()

    def __new__(cls, *args, **kwargs):
        view_func = args[1]
        if view_func in cls.views:
            raise Exception("View already in use!")
        
        if not callable(view_func):
            raise Exception("URL patterns requires callable!")

        cls.views.append(view_func)
        instance = super(RoutePattern, cls).__new__(cls)
        return instance
    
    def __init__(self, url_pattern, view_func, *args, **kwargs):
        self.url_pattern = url_pattern
        self.view_func = view_func
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def add_route(cls, url_pattern, view_func, *args, **kwargs):
        route_pattern_obj = cls(url_pattern, view_func, args, kwargs)
        return route_pattern_obj

    def resolve(self):
        # Here can be made some changes before substituting pattern
        # by resolver
        resolve_url = self.url_resolver.apply_middlewares(self.url_pattern)

        # Ready to match url_pattern
        resolved_url = resolve_url()
        return resolved_url
    
    
class RouteResolver:

    def __init__(self, url_patterns):
        self.url_patterns = url_patterns
        
    def match(self, url):
        # Search for match in URL patterns, basing on Request URL
        for pattern in self.url_patterns:
            resolved_url_pattern = pattern.resolve()
        
            match = re.fullmatch(resolved_url_pattern, url)
            if not match:
                continue
            
            # Success, return RouteMatch object which encapsulates
            # information needed to generate Response
            return RouteMatch(
                pattern.url_pattern,
                pattern.view_func,
                *match.groups(),
                **match.groupdict(),
                )
        
        # If there is no match after iteration, return None
        return None


class RouteMatch:

    def __init__(self, url_pattern, view_func, *args, **kwargs):
        self.url_pattern = url_pattern
        self.view_func = view_func
        self.args = args
        self.kwargs = kwargs


# class HttpResponse:
#     status_codes = {
#         200: "HTTP/1.1 200 OK\r\n",
#         404: "HTTP/1.1 404 NOT FOUND\r\n",
#     }

#     def __init__(
#             self,
#             request,
#             content,
#             status=status_codes.get(200),
#             *args, **kwargs
#             ):
#         self.request = request
#         self.content = content
#         self.status = status
#         self.headers = kwargs
        
#     def __call__(self):
#         response = self.status
#         for header_name, value in self.headers.items():
#             response += f"{header_name}: {value}\r\n"
        
#         response += "\r\n\r\n"
#         response += self.content
#         return response
    

# def index_view(request):
#     # msg = f"<h1>Hello, {username}!\r\n\tYour ID is {client_id}.</h1>"
#     msg = f'<h1 color="red">Hello, World!</h1>'
#     headers = {
#         "Content-Type": "text/html"
#     }
#     response = HttpResponse(request, msg, **headers)
#     return response

# def not_found_view(request):
#     msg = "<h1>Not Found!</h1>"
#     response = HttpResponse(request, msg)
#     return response

# def agata_view(request, username):
#     msg = f"<h1>Witaj, {username}!</h1>"
#     return HttpResponse(request, msg)

# def kotlet_view(request, kotlet):
#     msg = f"<h1>Zajebisty kotlet {kotlet}.</h1>"
#     return HttpResponse(request, msg)

# class StrPlaceholder:
#     _type = str


# class IntPlaceholder:
#     _type = int


# class FloatPlaceholder:
#     _type = float


# class RegexPlaceholderMiddleware:
#     placeholders = {
#         "str": StrPlaceholder(),
#         "int": IntPlaceholder(),
#         "float": FloatPlaceholder(),
#     }

#     # Define placeholder RegEx and Pattern object
#     placeholder_pattern = r"<(?P<type>\w+):(?P<name>\w+)>"
#     pattern_obj = re.compile(placeholder_pattern)

#     def apply(self, url_pattern):
#         # Function used on compiled regex Pattern object 
#         def replace(match):
#             placeholder_type, name = match.groups()
#             placeholder_obj = self.placeholders.get(placeholder_type)
#             if not placeholder_obj:
#                 raise Exception("Invalid URL Argument Type!")

#             replacement = rf"(?P<{name}>[^/]\w+)"
#             return replacement
            
        
#         return self.pattern_obj.sub(replace, url_pattern)


# class URLRegexResolver:
#     middlewares = [
#         RegexPlaceholderMiddleware(),
#     ]

#     def apply_middlewares(self, url_pattern):
#         def func():
#             # Variable holding updated url_pattern
#             resolved_url = url_pattern
#             for middleware in self.middlewares:
#                 # After each iterations, middleware substitutes part with
#                 # matched pattern and updates changes by overriding resolved_url
#                 resolved_url = middleware.apply(resolved_url)
            
#             return resolved_url
#         return func

# url_patterns = [
#     RoutePattern.add_route("/home/", index_view),
#     RoutePattern.add_route("/witaj/<str:username>/", agata_view),
#     RoutePattern.add_route("/kotlet/<str:kotlet>/", kotlet_view),
# ]


# class RequestParser:
    
#     def parse_request(self, request_str: str):
#         # Split Request on new line tokens and exctract first line
#         # for defining Request method, location and Protocol version
#         headers_list = request_str.strip().split("\n")
#         initial_header = headers_list.pop(0)

#         method, _, right = initial_header.partition(" ")
#         path, _, http_ver = right.partition(" ")

#         request_dict = {
#             "method": method,
#             "path": path,
#             "http_ver": http_ver,
#         }

#         # Iterate over list of headers and split at collon,
#         # Exract header name and its corresponding value
#         for header in headers_list:
#             header_name, value = header.split(":", 1)
#             request_dict[header_name] = value

#         return request_dict


# class ViewDispatcher:
#     # Default Not Found View
#     default_http_404 = not_found_view
#     request_parser = RequestParser()

#     def __init__(self, url_patterns, route_resolver):
#         self.url_patterns = url_patterns
#         self.route_resolver = route_resolver

#     def dispatch(self, request):
#         # Transform Request to a Dictionary
#         request_dict = self.request_parser.parse_request(request)

#         # Extract path, and match pattern agains url_patterns
#         path = request_dict["path"]
#         match = self.route_resolver.match(path)
#         if not match:
#             return None
            
#         view_func = match.view_func
#         args = match.args
#         kwargs = match.kwargs
        
#         return view_func(request_dict, *args)


# class Application:
#     # Main Components
#     route_resolver = RouteResolver()
#     dispatcher = ViewDispatcher(url_patterns, route_resolver)

#     def handle_request(self, request):
#         response = self.dispatcher.dispatch(request)
#         # If there was no response, that means that request for
#         # particular URL not match any of the declared patterns, hence
#         # return default HTTP 404
#         if not response:
#             response = self.dispatcher.default_http_404()
#             return response()
        
#         return response()

