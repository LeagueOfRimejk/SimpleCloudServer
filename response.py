class HttpResponse:
    status_codes = {
        200: "HTTP/1.1 200 OK\r\n",
        404: "HTTP/1.1 404 NOT FOUND\r\n",
    }

    def __init__(
            self,
            request,
            content,
            status=200,
            *args, **kwargs
            ):
        self.request = request
        self.content = content
        self.status = status
        self.headers = kwargs
        
    def __call__(self):
        response = self.status_codes.get(self.status)
        for header_name, value in self.headers.items():
            response += f"{header_name}: {value}\r\n"
        
        response += "\r\n"
        if type(self.content) == bytes:
            return response, self.content

        response += self.content
        return response, None