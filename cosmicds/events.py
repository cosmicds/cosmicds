from glue.core.message import Message


class StepChangeMessage(Message):
    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._value = value

    @property
    def value(self):
        return self._value
