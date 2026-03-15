import transpose_song as ts
import pytest

def test_is_not_a_chord_line():
    wl = {"m", "sus", "maj"}  # case-insensitive in loader; keeping lower here
    nc = {"x2", "repeat"}
    assert ts.is_chord_line("Oh dear what can the matter be", wl, nc) is False

@pytest.mark.parametrize("line", [
    "    Em                      F#m       Em    Asus4 A",
    "D Em G D x2",
    "D Em G D (x2)",
    "D Em G D x2:",
    "D Em G D ×2",
])
def test_is_a_chord_line_variants(line):
    wl = {"m", "sus", "maj"}
    nc = {"x2", "repeat"}
    assert ts.is_chord_line(line, wl, nc) is True
