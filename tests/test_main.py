import subprocess
import os


run_script = os.getenv("TASK3_RUN", "python src/main.py").split()


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


def test_three_different_params():
    process = subprocess.Popen(
        [*run_script, "1", "2", "3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    input_text = "Available moves"
    output, _ = process.communicate(input=input_text)

    assert input_text in output
