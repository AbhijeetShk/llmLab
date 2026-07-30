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

        if self.session.is_finished():

            raise StopIteration

        if not self.started:

            self.session.start()

            self.started = True

        else:

            self.session.step()

        token = self.session.current_token()

        if token is None:

            raise StopIteration

        return token