import random
class ShuffleQueue:
    def __init__(self, items):
        self.items = items
        self.queue = []

    def refill(self):
        self.queue = self.items[:]
        random.shuffle(self.queue)

    def next(self):
        if not self.queue:
            self.refill()
        return self.queue.pop()

    def __repr__(self):
        return f"ShuffleQueue(size={len(self.queue)}, items={self.queue})"