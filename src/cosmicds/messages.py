from glue.core.message import Message


class WriteToDatabaseMessage(Message):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StepChangeMessage(Message):
    def __init__(self, step, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._step = step

    @property
    def step(self):
        return self._step


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


class NewViewerMessage(Message):
    def __init__(self, viewer_class, data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._viewer_class = viewer_class
        self._data = data

    @property
    def viewer_class(self):
        return self._viewer_class

    @property
    def data(self):
        return self._data
