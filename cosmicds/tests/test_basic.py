import pytest
from testbook import testbook
from pathlib import Path
from os.path import join

from jupyter_client import KernelManager
km = KernelManager()
km.connection_file = "kernel-cosmicdstest.json"

directory = str(Path(__file__).parent)

@pytest.fixture(scope='module')
def tb():
    with testbook(join(directory, "test_basic.ipynb"), execute=True, km=km) as tb:
        yield tb

# def test_instantiate(tb):
#     instantiate = tb.ref("test_instantiate")
#     assert instantiate()

# def test_server_url(tb):
#     get_url = tb.ref("server_url")
#     assert get_url() == ""

# def test_ipykernel_filename(tb):
#     get_fname = tb.ref("ipykernel_filename")
#     assert get_fname().startswith("kernel")

# def test_servernames(tb):
#     get_servers = tb.ref("server_names")
#     print(get_servers())
#     assert get_servers()[0]["base_url"] == ['kernel-cosmicdstest.json']


def test_kernel_id(tb):
    kernel_id = tb.ref("kernel_id")
    assert kernel_id() == 'cosmicdstest'

