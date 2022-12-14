"""A module to run both black and docformatter."""

import sys
from click.testing import CliRunner
from io import StringIO
from black import main as black_main
from docformatter import _main as doc_main


def run_black():
    runner = CliRunner(mix_stderr=False)
    argv = sys.argv[1:]
    result = runner.invoke(black_main, argv)
    assert result.exit_code == 0
    return result.stdout


def run_doc():
    argv = [v for v in sys.argv if not v.startswith("--")]
    out = StringIO()
    doc_main(argv, out, sys.stderr, sys.stdin)
    return out.getvalue()


# Linebreak (\n) is appended by print function.
if diff_black := run_black().rstrip():
    # Apply Black and ignore docformat to avoid conflicted diff.
    print(diff_black)
elif diff_doc := run_doc().rstrip():
    # Display docformatter result (with \n appended)
    print(diff_doc)
else:
    # no line break to show
    pass
