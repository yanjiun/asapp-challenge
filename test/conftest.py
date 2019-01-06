import pytest
import subprocess
from ..challenge import main
from ..initialize_db import create_db


@pytest.fixture(scope="module")
def start_server():
    create_db("test.db")
    main("test.db")
    yield None
    subprocess.run(["rm", "../test.db"])

