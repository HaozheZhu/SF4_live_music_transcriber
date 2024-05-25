import fractions
from quickly.dom import lily

def create_lilypond_file(music): 
    # Create a header
    header = lily.Header()
    header.title = 'Generated Music'
    header.composer = 'hz403 and rw680'
    header.tagline = False

    # the actual music
    output = music.write_indented()
    
    # write to file
    with open('./software/tmp/lilypond_file.ly', 'w') as f:
        f.write('\\version "2.18.2"\n')
        f.write(header.write_indented())
        f.write(output)
        print('Lilypond file created at ./software/tmp/lilypond_file.ly')

if __name__ == "__main__":
    music = lily.Document(lily.MusicList())
    music[0].append(lily.Note('c',
                              lily.Octave(1), # octave relative to C3 i.e. 0 is C3
                              lily.Duration(fractions.Fraction(1, 8)), 
                              )
                    )
    music[0].append(lily.Note('d', lily.Duration(fractions.Fraction(1, 8))))
    music[0].append(lily.Note('e', lily.Duration(fractions.Fraction(1, 4))))
    music[0].append(lily.Note('f', lily.Duration(fractions.Fraction(1, 2))))
    music[0].append(lily.Note('f', lily.Duration(fractions.Fraction(1, 2))))


    create_lilypond_file(music)