from music21 import *
# https://www.music21.org/music21docs/usersGuide/usersGuide_01_installing.html
s = corpus.parse('bach/bwv65.2.xml')
print(s.analyze('key'))
s.show() # best to run this from cli, not e.g. VSCode


