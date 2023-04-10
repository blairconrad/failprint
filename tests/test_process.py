"""Tests for the `process` module."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis.strategies import characters, text

from failprint import WINDOWS
from failprint.capture import Capture
from failprint.process import run_pty_subprocess, run_subprocess


def test_run_list_of_args_as_shell() -> None:
    """Test that a list of arguments is stringified."""
    code, output = run_subprocess(["python", "-V"], shell=True)
    assert code == 0
    assert "Python" in output


def test_run_unknown_shell_command() -> None:
    """Run an unknown command in a shell."""
    code, output = run_subprocess("mlemlemlemlemle", shell=True)
    assert code > 0
    assert output


def test_run_unknown_command() -> None:
    """Run an unknown command without a shell."""
    # maybe this exception should be caught in the code?
    with pytest.raises(FileNotFoundError):
        run_subprocess("mlemlemlemlemle")


@pytest.mark.skipif(WINDOWS, reason="no PTY support on Windows")
def test_run_pty_subprocess_capture_none(capsys: pytest.CaptureFixture) -> None:
    """Run a PTY subprocess without capturing output.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    code, output = run_pty_subprocess(["bash", "-c", "echo PTY"], capture=Capture.NONE)
    assert code == 0
    assert not output
    outerr = capsys.readouterr()
    assert "PTY" in outerr.out


@given(text(alphabet=characters(blacklist_categories="C")))
def test_pass_stdin_to_subprocess(stdin: str) -> None:
    """Pass input to a normal subprocess.

    Arguments:
        stdin: Text sample generated by Hypothesis.
    """
    code, output = run_subprocess(["cat"], stdin=stdin)
    assert code == 0
    assert output == stdin


@pytest.mark.skipif(WINDOWS, reason="no PTY support on Windows")
@given(text(alphabet=characters(blacklist_categories="C")))
@settings(deadline=None)
def test_pass_stdin_to_pty_subprocess(stdin: str) -> None:
    """Pass input to a PTY subprocess.

    Arguments:
        stdin: Text sample generated by Hypothesis.
    """
    code, output = run_pty_subprocess(["cat"], stdin=stdin)
    assert code == 0
    assert output == stdin
