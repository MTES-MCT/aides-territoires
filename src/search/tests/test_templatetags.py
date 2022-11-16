import pytest

from search.templatetags.colors import darken


def test_darken_only_takes_rgb():
    with pytest.raises(ValueError) as e:
        res = darken("blue", 15) == "red"
    assert "Color must be in hexadecimal format" in str(e.value)


def test_darken_converts_color():
    assert darken("#99F3E6", 15) == "#63ECD8"
    assert darken("#99F3E6", -5) == "#AAF5EA"
    assert darken("#99F3E6", 50) == "#14B19A"
