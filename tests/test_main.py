import subprocess
import os
import pytest


run_script = os.getenv("TASK3_RUN", "python src/main.py").split()


@pytest.fixture(autouse=True)
def run_before_and_after_tests(request):
    if "noautofixt" in request.keywords:
        print("NONE ", end="")
        yield
        return

    os.environ["RICH_DISABLE_ANSI"] = "1"
    os.environ["SLEEP"] = "0"
    yield
    del os.environ["RICH_DISABLE_ANSI"]
    del os.environ["SLEEP"]


def test_without_params():
    result = subprocess.run(run_script, capture_output=True, text=True)
    assert result.returncode != 0
    assert "Not enough arguments" in result.stderr


def test_one_param():
    result = subprocess.run([*run_script, "1"], capture_output=True, text=True)
    assert result.returncode != 0
    assert "Not enough arguments" in result.stderr


def test_repeated_param():
    result = subprocess.run(
        [*run_script, "1", "1", "2", "3", "4"], capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "Arguments must be different" in result.stderr


def test_even_params():
    result = subprocess.run(
        [*run_script, "1", "2", "3", "4"], capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "must be an odd" in result.stderr


@pytest.mark.noautofixt
def test_three_different_params():
    process = subprocess.Popen(
        [*run_script, "1", "2", "3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    output, _ = process.communicate()

    input_text = "Available moves"
    assert input_text in output
