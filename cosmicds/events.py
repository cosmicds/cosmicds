from glue.core.message import Message


class StepChangeMessage(Message):
    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._value = value

    @property
    def value(self):
        return self._value


class LoadDataMessage(Message):
    def __init__(self, path, label, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._path = path
        self._label = label

    @property
    def path(self):
        return self._path

    @property
    def label(self):
        return self._label
