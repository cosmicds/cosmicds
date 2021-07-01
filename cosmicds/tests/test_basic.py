import pytest


def test_instantiate():
    from cosmicds.app import Application
    from glue.core.state_objects import State

    app = Application()

    assert issubclass(type(app.state), State)