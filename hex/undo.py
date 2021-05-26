class Undo:
    def __init__(self):
        self.stack = []
        self.index = -1

    def record_action(self, data):
        self.stack.append(data)
        self.index += 1

    def undo(self):
        index = self.index
        self.index -= 1
        return self.stack[index]

    def redo(self):
        index = self.index
        self.index += 1
        return self.stack[index]
