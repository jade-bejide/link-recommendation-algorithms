import heapq

class PriorityQueue:
    def __init__(self):
        self.queue = {}

    def enqueue(self, node: int, val: float):
        self.queue[node] = val

    def get_top_n(self, n: int):
        return heapq.nlargest(n, self.queue.keys(), key=lambda node: self.queue[node])
