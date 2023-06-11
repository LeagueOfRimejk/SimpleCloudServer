class EmptyInput(Exception):
    ...

class TerminateTokenization(Exception):
    ...

class MissingRootTokenNode(Exception):
    ...


COMMAND_TEMPLATE = {
    "register": {
        "description": "",

        "usage": [

        ],

        "flags": {
            
        },

        "subcommands": {
    
        },

        "input": {
            
        },
    },
}

# User Commands Meta Data
USER_COMMANDS = {
    "register": {
        
        "description": "Register a new User",
        "usage": [
            "register -u [USERNAME] -p [PASSWORD]",
            "register --username [USERNAME] --password [PASSWORD]",
        ],
        "flags": {
            "-u": {"description": "Username", "required": True},
            "--username": {"description": "Username", "required": True},

            "-p": {"description": "Password", "required": True},
            "--password": {"description": "Password", "required": True},
        },
        "subcommands": {},
        "input": {
            "slots": 2,
        },
    },
}

# Commands Meta Data Entry
__COMMANDS__ = {
    **USER_COMMANDS,
}

class TokenGroup:
    _USER = "USER"
    _ROOM = "ROOM"
    _FLAG = "FLAG"
    _ARGUMENT = "ARGUMENT"

class TokenCategory:
    _COMMAND = "COMMAND"
    _FLAG = "FLAG"
    _ARGUMENT = "ARGUMENT"

_user_group = TokenGroup._USER
USER_TOKENS = {
    "register": (_user_group, TokenCategory._COMMAND),
    "join": (_user_group, TokenCategory._COMMAND),
}

_flag_group = TokenGroup._FLAG
FLAG_TOKENS = {
    "-u": (_flag_group, TokenCategory._FLAG),
    "--username": (_flag_group, TokenCategory._FLAG),

    "-p": (_flag_group, TokenCategory._FLAG),
    "--password": (_flag_group, TokenCategory._FLAG),
}

# Tokens Meta Data Entry
__TOKENS__ = {
    **USER_TOKENS,
    **FLAG_TOKENS,
}

class Token:

    def __init__(self, name, group, category):
        self.name = name
        self.group = group
        self.category = category
        self._next = None
        self.is_root = False

    def link(self, token_instance):
        self.next = token_instance

    @property
    def next(self):
        return self._next
    
    @next.setter
    def next(self, value):
        self._next = value


class TokenFactory:
    default_token = TokenGroup._ARGUMENT, TokenCategory._ARGUMENT

    def ensure_list(self, user_input: any):
        if type(user_input) != str:
            raise TerminateTokenization

        command_list = str(user_input).strip().split()
        if len(command_list) < 1:
            raise EmptyInput

        return command_list

    def create_token(self, command: str, *args, **kwargs):
        """
        Creates Token.

        :param kwargs["root"]: Set root node [True | False]
        """

        # Check optional root parameter
        root = kwargs.get("root", False)
        group, category = __TOKENS__.get(command, self.default_token)
        token = Token(command, group, category)
        token.is_root = root
        return token
    
    def generate(self, user_input):
        try:
            # Ensure that provided input will be list
            command_list = self.ensure_list(user_input)
            
            # Root node for further validation
            root_node = self.create_token(command_list[0], root=True)

            curr_node = root_node
            for command in command_list[1:]:
                token = self.create_token(command, root=False)

                # Link Token
                curr_node.link(token)
                curr_node = token

        except EmptyInput:
            ...

        except TerminateTokenization:
            ...

        else:
            return root_node
        

class TokenValidator:

    def validate(self, root_token: Token):
        if not root_token.is_root:
            raise MissingRootTokenNode
        
        if root_token.category == TokenCategory._ARGUMENT:
            return root_token
        
        commands_tree = __COMMANDS__
        curr_token = root_token
        flag_token = None
        while curr_token:
            group, category = curr_token.group, curr_token.category

        


class AbstractCommand:

    def execute(self, data):
        raise NotImplementedError
    
    def help(self):
        raise NotImplementedError
    
    def invalid_input(self, input):
        raise NotImplementedError
    
    def invalid_flag(self, flag):
        raise NotImplementedError


if __name__ == "__main__":
    factory = TokenFactory()
    user_input = "register --username Knaga -p random123"
    # user_input = "srakas"
    token_linked_list = factory.generate(user_input)
    
    token_node = token_linked_list
    while token_node:
        print(token_node.name, token_node.group, token_node.category)
        token_node = token_node.next

    




