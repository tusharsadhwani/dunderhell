import ast
import os.path
import subprocess
import sys

import pytest

import dunderhell


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Generates all dunderhell tests based on files in the test_files folder."""
    test_files_path = os.path.join(os.path.dirname(__file__), "test_files")

    test_params: list[tuple[str, str]] = []
    for file_name in os.listdir(test_files_path):
        if not file_name.endswith(".py"):
            continue
        if file_name.endswith(".result.py"):
            continue

        file_path = os.path.join(test_files_path, file_name)
        autofixed_file_path = file_path.removesuffix(".py") + ".result.py"
        if not os.path.exists(autofixed_file_path):
            raise AssertionError(f"Expected {autofixed_file_path} to exist")

        test_params.append((file_path, autofixed_file_path))

    metafunc.parametrize(("file_path", "dunderified_file_path"), test_params)


def test_dunderhell(file_path: str, dunderified_file_path: str) -> None:
    """
    Ensure that `foo.py` dunderified becomes `foo.result.py`, and the output of
    running both files is identical.
    """
    with open(file_path) as file, open(dunderified_file_path) as dunderified_file:
        contents = file.read().rstrip("\n")
        dunderified_contents = dunderified_file.read().rstrip("\n")

    tree = ast.parse(contents)
    dunderhell.dunderify(tree)
    output_contents = ast.unparse(tree)
    assert output_contents == dunderified_contents

    # Run both the original and dunderified scripts and ensure same output
    python = sys.executable
    expected_output = subprocess.check_output([python, "-c", contents])
    dunderified_output = subprocess.check_output([python, "-c", dunderified_contents])
    assert expected_output == dunderified_output
