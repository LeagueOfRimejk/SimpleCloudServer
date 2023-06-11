class RequestParser:
    
    def parse_request(self, request_str: str):
        # Split Request on new line tokens and exctract first line
        # for defining Request method, location and Protocol version
        headers_list = request_str.strip().split("\r\n")
        initial_header = headers_list.pop(0)

        method, _, right = initial_header.partition(" ")
        path, _, http_ver = right.partition(" ")

        request_dict = {
            "method": method,
            "path": path,
            "http_ver": http_ver,
        }

        # Iterate over list of headers and split at collon,
        # Exract header name and its corresponding value
        for header in headers_list:
            header_name, value = header.split(":", 1)
            request_dict[header_name] = value

        return request_dict