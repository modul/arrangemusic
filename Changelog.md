2011/04/13 v0.4.2

* Improved configuration code and changed some options, removed ignore-articles (always done)
* Default pattern section in configuration is 'default-pattern', when it exists
* Added {artist}, {article}, {theartist} and removed {extension}
* Returning no path on unknown file extension
* Renamed modules, package and rearranged code
* Some minor improvements to output and code in general
* Using nosetests and lettuce (for fun)
* Using version info derived from git tags and commit count (git describe)

2011/04/06 v0.4.1

* some code updates and fixes
* made configuration a singleton opject
* more object orientation
* code cleannig

2011/04/05 v0.4

* Changelog is still handy
* complete rewrite, much more code but I think its more clean and versatile now…
* unittests (well, a few)
* using python to find files
* instead of single/multiartist patterns, multiple (n) user-definable 
  patterns are possible now
* enhanced options, better help text
* using placeholders like {artist}, {title} in patterns (thanks to python’s str.format())

2011/02/28 

* everything under git control now
* finds flac files now as well
* from here on, read git log

2010/02/18 v0.3.9

* first improvements for more than 4 years ;)
* put script under the beerware license
* replaced tag wrapper class by the tagpy (python-tag - python bindings
  for taglib) package - this also means that more file types are supported, see tagpy
  documentation or the one of taglib, at least ogg, mp3, flac...
* can work recursively now using 'find' to get a listing of mp3 and ogg files
* moved all configuration to a file (~/.arrangemusic.py or default.cfg in the build dir)
* defaults of commandline switches are configurable
* two path rewrite patterns available: multiartist and singleartist
* added commandline switches -1 and -2 to choose between multiartist and
  singleartist pattern
* commandline switches can be turned off as well now, meaning: -n turns pretend
  mode on, -N turns it off, etc. This should be used to overwrite configuration
  defaults.
* CTRL-C is caught. Script just terminates without the python exception
  message.

2005/12/16

* new pattern: %Y (year styling) and %B (album styling), same as with %T (tracknumber styling); 
  changed ___cfg_trknum to ___cfg_trkstyle, for %Y it is ___cfg_yrstyle, for %B it's __cfg_albstyle

2005/12/05 v0.3.2

* bug with special chars (Bug 01) was fixed
  need to take more look at charsets and locales...
* simplified the moving/copying part (just code-cleaning)
* created a Changelog.txt, TODO.txt and a BUGS.txt ;)

2005/11/24 v0.3.1

* new feature "article ignoring": if %1a is used, it is probably not meant to be the "T"
  from "The Who" but the "W". It's the same for other languages. I added the option
  to switch this shifting on and there's a list where you can enter some common articles.
  "The" and "Die" (german) is already in that list ;)
* if the first OR second "word" is a number, you may specify if the first digit, the whole
  number, the first letter of the article (if number comes 2nd), or something else shall be substituted
  with %1a

2005/10/14 v0.3

* added new pattern: %1a, will be replaced by the first letter of the artist
  it's now possible to arrange files like: S/some_artist/any_album/a_track.mp3 e.g.

2005/04/19 v0.2.3

* if the destination file already exists, it will be asked to overwrite it

2005/04/16 v0.2.2:

* wrote a wrapper for tags, to support _OGG_Vorbis_ (tags.py)
* add "..." to strings of 30 chars to make ugly shortened ID3v1 strings more nice (MP3 only)
  .oO( Pls gimme ID3v2 support :-/ )

2005/04/05 v0.2.1:

* using python functions for moving and copying files now (shutil.move(), shutil.copy()) 

2005/03/29 v0.2:

* added option "-m" (credits to jb)
* added option "-t" 
* cleaned code
* using gnu_getopt now -> mixing of argument and options is possible (i.e. script.py option FILE option option)
* added option "-i"

2004/06/19 v0.0/0.1:

* first "kind of"-working code written
* needed it to arrange my music copied from a backup back to harddisk
  (after I unwillingly did rm -rf /mnt/music :( )
  
