class BatchManager:

    def __init__(self):

        self.active = []

    def add(self, session):

        self.active.append(session)

    def remove_finished(self):

        self.active = [
            s
            for s in self.active
            if not s.is_finished()
        ]

    def batch(self):

        return self.active