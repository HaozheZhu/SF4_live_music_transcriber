#!/bin/sh
lilypond -o ./software/tmp/out ./software/tmp/lilypond_file.ly
evince ./software/tmp/out.pdf