class DynamicBatchScheduler:

    def __init__(self):

        self.active = []

    def add(
        self,
        session,
    ):

        self.active.append(
            session
        )

    def remove_finished(self):

        self.active = [

            session

            for session in self.active

            if not session.is_finished()

        ]

    def batch(
        self,
    ):

        return self.active