class MPC_API:
    def __init__(self):
        self.handlers = {}

    def get_key(self, value):
        return value.lower()

    def handle(self, action: str, httpMethod="GET"):
        def decorator(func):
            self.add_handler(func, action, httpMethod)
            return func
        return decorator

    def add_handler(self, fun, action, httpMethod):
        if action in self.handlers:
            self.handlers[self.get_key(action)][self.get_key(httpMethod)] = fun
        else:
            self.handlers[self.get_key(action)] = {self.get_key(httpMethod) : fun}


