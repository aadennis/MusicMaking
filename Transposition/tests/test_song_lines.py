import transpose_song

song_line_lyric = "Oh dear what can the matter be"
song_line_chordset = "    Em                      F#m       Em    Asus4 A"

def test_is_not_a_chord_line():
    result =  transpose_song.is_chord_line(song_line_lyric)
    assert result == False

def test_is_a_chord_line():
    result = transpose_song.is_chord_line(song_line_chordset)
    assert result == True