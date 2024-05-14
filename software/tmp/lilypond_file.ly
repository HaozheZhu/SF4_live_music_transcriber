\version "2.24.3"

\header { }

melody = {
  \clef treble
  \key c \major
  \time 4/4

  a' b' c'' d' a' r4. f''8
}

\score {
  \new Staff \melody
  \layout { }
  \midi { }
}

