import re


class StrPlaceholder:
    _type = str


class IntPlaceholder:
    _type = int


class FloatPlaceholder:
    _type = float


class RegexPlaceholderMiddleware:
    placeholders = {
        "str": StrPlaceholder(),
        "int": IntPlaceholder(),
        "float": FloatPlaceholder(),
    }

    # Define placeholder RegEx and Pattern object
    placeholder_pattern = r"<(?P<type>\w+):(?P<name>\w+)>"
    pattern_obj = re.compile(placeholder_pattern)

    def apply(self, url_pattern):
        # Function used on compiled regex Pattern object 
        def replace(match):
            placeholder_type, name = match.groups()
            placeholder_obj = self.placeholders.get(placeholder_type)
            if not placeholder_obj:
                raise Exception("Invalid URL Argument Type!")

            replacement = rf"(?P<{name}>[^/][\w\.]+)"
            return replacement
            
        
        return self.pattern_obj.sub(replace, url_pattern)


class URLRegexResolver:
    middlewares = [
        RegexPlaceholderMiddleware(),
    ]

    def apply_middlewares(self, url_pattern):
        def func():
            # Variable holding updated url_pattern
            resolved_url = url_pattern
            for middleware in self.middlewares:
                # After each iterations, middleware substitutes part with
                # matched pattern and updates changes by overriding resolved_url
                resolved_url = middleware.apply(resolved_url)
            
            return resolved_url
        return func