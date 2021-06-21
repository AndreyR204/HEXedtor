class Undo:
    def __init__(self):
        self.stack = []
        self.index = -1

    def record_action(self, data):
        self.stack.append(data)
        self.index += 1

    def undo(self):
        try:
            self.index -= 1
            return self.stack[self.index]
        except IndexError:
            return self.stack[0]

    def redo(self):
        try:
            self.index += 1
            return self.stack[self.index]
        except IndexError:
            return self.stack[len(self.stack)-1]
