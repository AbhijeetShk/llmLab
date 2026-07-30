from .session import GenerationSession


class StreamIterator:

    def __init__(
        self,
        session: GenerationSession,
    ):

        self.session = session

        self.started = False

    def __iter__(self):

        return self

    def __next__(self):

        if not self.started:

            self.session.start()

            self.started = True

        while True:

            delta = self.session.next_text_chunk()

            if delta:

                return delta

            if self.session.is_finished():

                raise StopIteration

            self.session.step()