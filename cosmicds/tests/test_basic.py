from testbook import testbook
from pathlib import Path
from os.path import join

directory = str(Path(__file__).parent)

@testbook(join(directory, "test_basic.ipynb"), execute=True)
def test_instantiate(tb):
    instantiate = tb.ref("test_instantiate")
    assert instantiate()
