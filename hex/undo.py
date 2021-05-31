class Undo:
    def __init__(self):
        self.stack = []
        self.index = -1

    def record_action(self, data):
        self.stack.append(data)
        self.index += 1

    def undo(self):
        self.index -= 1
        return self.stack[self.index]

    def redo(self):
        self.index += 1
        return self.stack[self.index]
