import pytest

from snippet import utils


@pytest.mark.parametrize(
    "value,expected",
    [
        ("""Wow""", "Wow"),
        ("""""", None),
        (
            """Hey
        # Nope""",
            "Hey",
        ),
        (
            """Wow
# Commit message editor
# ignore lines
""",
            "Wow",
        ),
    ],
)
def test_ignore_lines(value, expected):
    result = utils.ignore_lines(value)
    assert result == expected
