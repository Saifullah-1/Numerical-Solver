class Error:
    def __init__(self, msg):
        self.msg = msg

    def execute(self):
        return self.msg
