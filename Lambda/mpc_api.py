class MPC_API:
    def __init__(self):
        self.handlers = {}

    def get_key(self, action):
        return action

    def handle(self, action):
        def decorator(func):
            # print("inside")
            self.add_handler(func, action)
            return func
        return decorator

    def add_handler(self, fun, action):
        self.handlers[self.get_key(action)] = fun

