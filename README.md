# Python Pillow Pov Processor

Various bits and bobs of video processing code that I've had as single scripts
for years and years and years (you can tell how old it is by the fact it uses
Pov-Ray) brought together as an integrated script fro adding "special effects" to
video.

It reads a bunch of input clips using ffmpeg and output it's results in
arbitrary length clips again using ffmpeg.

In between input and output, it can stretch the duration of the input clips,
process the individual frames with PIL/Pillow for simple effects and feed the
frames through my digital rostrum camera™ which employs POV-Ray.

As it stands, it's for my own use and isn't exactly robust or intuitive to use.
But it might be useful as a framework for your own processing???

There's a Docker container included that handles all the dependencies.
You can either use it as-is or as a list of what modules you need to install.
