class MPC_API:
    def __init__(self):
        self.handlers = {}

    def get_key(self, action):
        return action

    def handle(self, action):
        def decorator(func):
            print("inside")
            self.add_handler(func, action)
            return func
        return decorator

    def add_handler(self, fun, action):
        self.handlers[self.get_key(action)] = fun


api = MPC_API()


@api.handle("Message")
def function(event):
    print("Message")
    return event


@api.handle("Post")
def function(event):
    print("Post")
    return event


@api.handle("GET")
def function(event):
    print("GET")
    return event


if __name__ == "__main__":
    api.handlers["Message"](None)
    api.handlers["Post"](None)
    api.handlers["Message"](None)


