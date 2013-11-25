PasswordGenerator
=================

Generates all possible password strings with  a seed file and and a template word.

**Usage**

```
usage: ./generate.py [OPTIONS] -s <seedfile> -t <template string>

Password generator with seed chars and templates

optional arguments:

  -h, --help            show this help message and exit
  -t PWDTEMPLATE, --template PWDTEMPLATE
                        Template word to fill up with the seed chars
  -s SEEDFILE, --seed SEEDFILE
                        File name with the seed letters
  -o OUTFORMAT, --outputformat OUTFORMAT
                        TODO: Output format of the generated passwords
                        (sqlite|text|screen). Default is screen.
  -f OFILE, --file OFILE
                        Output file name to store results

```
