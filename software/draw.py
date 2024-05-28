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

def draw_example():
    music = lily.Document(lily.MusicList())
    music[0].append(lily.Note('Cis',
                              lily.Octave(1), # octave relative to C3 i.e. 0 is C3
                              lily.Duration(fractions.Fraction(1, 8)), 
                              )
                    )
    music[0].append(lily.Note('D',
                              lily.Octave(1), # octave relative to C3 i.e. 0 is C3
                              lily.Duration(fractions.Fraction(1, 8)), 
                              )
                    )
    music[0].append(lily.Note('e',
                              lily.Octave(1), # octave relative to C3 i.e. 0 is C3
                              lily.Duration(fractions.Fraction(1, 2)), 
                              )
                    )
    music[0].append(lily.Note('f',
                              lily.Octave(1), # octave relative to C3 i.e. 0 is C3
                              lily.Duration(fractions.Fraction(1, 4)), 
                              )
                    )
    music[0].append(lily.Note('cis',
                              lily.Octave(1), # octave relative to C3 i.e. 0 is C3
                              lily.Duration(fractions.Fraction(1, 1)), 
                              )
                    )
    
    create_lilypond_file(music)

def string_to_lilypond(string): # string = e.g. 'c#3'
    chars = list(string)
    octave = int(chars[-1])
    note = chars[0].lower()
    accidental = ''
    if len(chars) == 3:
        if chars[1] == '#':
            accidental = 'is'
        else:
            accidental = 'es'
    return note+accidental, octave

def add_note_to_music(note_accidental, octave, duration, music):
    music[0].append(lily.Note(note_accidental,
                              lily.Octave(octave-3), # octave relative to C3 i.e. 0 is C3
                              lily.Duration(fractions.Fraction(duration)), 
                              )
                    )
    
def draw_music(note_string_list, note_duration_list):
    music = lily.Document(lily.MusicList())
    
    for note_string, duration in zip(note_string_list, note_duration_list):
        note_accidental, octave = string_to_lilypond(note_string)
        add_note_to_music(note_accidental, octave, duration, music)

    create_lilypond_file(music)

if __name__ == "__main__":
    # draw_example()
    note_string_list = ['C#5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6']
    note_duration_list = [0.125, 1/8, 0.25, 1/4, 1/4, 1/4, 1/4, 1]
    
    draw_music(note_string_list, note_duration_list)