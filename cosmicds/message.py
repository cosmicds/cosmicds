from glue.core.message import Message

__all__ = ["CDSLayersUpdatedMessage"]

class CDSLayersUpdatedMessage(Message):
    def __init__(self, sender, tag=None):
        super().__init__(sender, tag=tag)