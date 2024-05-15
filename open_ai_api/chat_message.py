class SystemMessage:
    def __init__(self, content):
        self.role = "system"
        self.content = content

    def json(self):
        return {"role": self.role, "content": self.content}


class UserMessage:
    def __init__(self, content):
        self.role = "user"
        self.content = content

    def json(self):
        return {"role": self.role, "content": self.content}
