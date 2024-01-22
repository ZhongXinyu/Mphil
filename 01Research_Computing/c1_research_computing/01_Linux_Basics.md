# Linux Terminal

In this section we are going to learn the basics of using the Linux/Unix Shell.  We need to learn how to use this <b>C</b>ommand <b>L</b>ine <b>I</b>nterface (CLI) as it is the fastest and simplest way to manage our environment and processes needed for our analysis piplines.  Many **G**raphical **U**ser **I**nterfaces (GUI) will claim to handle these tasks for you but they are generally slower to use than the CLI and the CLI allows far greater automation of complex tasks via scripts.  Finally you will need to master this if you plan to use any supercomputers as they all run Linux and the CLI is often the only way to access the system.  This guide is fairly brief but will give you enough to get up and running.

## What is the Linux Terminal?

Before we begin it will be useful to clarify the language surrounding this section.  You will very often hear the content of this lecture in courses called "Introduction to Linux" or something similar which is not entirely accurate.  Formally, Linux is actually a free, open source, Unix-like operating system kernel.  A kernel is the part of an operating system that is responsible for the lowest level tasks like: memory management, process management/task management, and disk management.  The Linux kernel forms the basis of several operating systems which are called Linux distributions like, Ubuntu, Fedora, Red Hat Enterprise Linux (RHEL) as well as Android and ChromeOS.  Mac and iOS use a very similar Unix-like kernel so are sometimes said to be based on Linux, but this is not the case.  Windows has its own kernel, but as of Windows 10 it includes a Linux subsystem that you can enable. We will not be learning anything about how to install or manage a Linux distribution or kernel in this course.

What we are going to be learning is "BASH" which stands for Bourne Again SHell.  BASH is typically the default login shell for Linux where a shell is a programme that allows the user to provide text commands directly to the operating system.  It is accessed via a **terminal** which is a programme that creates a window for the shell to run in.  If you are on a supercomputer it will almost certainly be running Linux and you will only access the system via a terminal running the BASH shell. This is where the confusion between shell, terminal and Linux comes from.

BASH is actually a programming language that contains many commands which directly connect to the operating system. If you are on Linux or Mac (note that ZSH is the default shell on macOS in recent versions but it works almost the same way) you can just open a terminal, if you are on Windows you will need to activate the Windows Subsystem for Linux (WSL) see here: https://learn.microsoft.com/en-us/windows/wsl/install

Now let's begin.
## Basics

When you open a terminal window you will get a window with a command prompt and you will usually be in your home directory.  Everything in the terminal is controled by commands, which are usually 2-3 letters long. The first thing we need to do is find out where we are so we use `pwd` (<b>p</b>rint <b>w</b>orking **d**irectory):

```bash
$ pwd
```

This tells us where we are.  Next we need to move to the folder where we want to work but first we need to know where we could go with `ls` (<b>l</b>i<b>s</b>t) which tells us what is in the directory we are in:

```bash
$ ls
```

Every command has a large list of options which control or modify the commands behaviour.  All BASH commands have them and they are added with the "`-`" prefix.  For example we could add `-a` (**a**ll) to show hidden files (ones beginning with a `.`, typically these are hidden for a reason as you shouldn't need to mess with them too often.  We will see some examples as we go through the course):

```bash
$ ls -a
```

To get a list of all possible options for a command you just need add `man` before it to consult the **man**ual pages

```bash
$ man ls
```
The manual is exited by typing "q".  The options (bit after the dash) can be combined together and input in any order.  For example to get the list in long format, by time, in reverse order, including hidden:

```bash
$ ls -ltra
```

---
**NOTE -- Permissions**

This list leads us to an important aspect of Linux which you need to consider when working with bash which is permissions.  The permissions for each file is described by the first 10-characters in long format (`drwxrwxrwx` would mean <b>d</b>irectory <b>r</b>ead <b>w</b>rite e<b>x</b>ecute at `user`, then `group`, then `other` level.  If a letter is replaced by `-` then the corresponding permission is denied for that set of users) which is followed by the owner, group, size, date last accessed, and filename.

The permissions are important as they protect you work and workspace from other users on the system.  Typically you would have `rwx` for user so you can read and edit your files as well as execute them (which just means run them, or for directories/folders open them), `r--` for group so people in your group can see your code but not edit or run it (directories will need `r_x` otherwise they will not be able to open them, omitting `w` means that they can't create new files in your directories) and `---` or `r--` for other depending on taste.  You should avoid making either `group` or `other` have `w` as it means that they can edit your stuff (or replace your text with viruses) or in the case of directories, dump unlimited content into your folders.  When you create a file it will probably default to `-rw-r--r--` as this is safe.  However, if it is a BASH script you will need to change it to `-rwxr--r--` in order to run it.

Permissions can be changed with `chmod`, which takes octal numbers as arguments, so 

```bash
$ chmod 644 filename
```

makes `filename` readable by anyone and writeable by the owner only. This because `6` in octal is `110` in binary which translates to `rw-` (`1` is on `0` off) for user, and 4 in octal is `100` in binary which translates to `r--` for everyone else so 644 is `-rw-r--r--`.  It also works in symbolic mode where the same command would be: 

```bash
$ chmod u=rw,go=r filename
``` 

see `man chmod` for many other options. The `d` cannot be changed (it's either a directory or it's not, and `chmod` can't do much about that).

You can also change the owner of files with `chown` which is used like:

```bash
$ chown "user" "folder/file"
```

And you can set the default permissions for new files with `umask`, e.g:

```bash
$ umask 644
```

---

For commands which interact with files you can append a pattern after the command to limit the action to just files which match this pattern. For example we can limit the previous command to just files called `hello.py` but appending it like this:

```bash
$ ls -ltra hello.py
```

or all files ending in `.py`:

```bash
$ ls -ltra *.py
```
---
**NOTE -- Wildcards**

Here we can define the pattern to contain wildcards, this is called `Globbing` (this is short for `global`, not that this name seems particularly relevent). Here `*` is a wildcard that can match any sequence of any number of characters (including none at all).  By characters we mean any symbol at all, not just letters. There are many other wildcards you can use including:

- `?` which matches one character so `ma?` would match "mat", "map" and "man" but not "mast".  

- `[]` matches any of the contents so `m[uao]m` matches "mum", "mam", "mom".  You can also use dash to indicate a range. So `[0-9]` matches any numeral and `[a-z]` matches any letter.  `!` negates the match so `[!9]` will match all but "9" and `^` will negate all in range so `[^1-4]` will match all but "1,2,3,4". There are also some standard (`POSIX`) sets you can use: [[:lower:]], [[:upper:]], [[:alpha:]], [[:digit:]], [[:alnum:]], [[:punct:]], and [[:space:]] which match: lowercase letters, uppercase letters, upper or lowercase letters, numeric digits, alpha-numeric characters, punctuation characters, and white space characters respectively. 

- `{}` is a list of things, comma separated without spaces. 

- `\` is used to make special symbols literal. So if you wanted to match `?` you would use `\?`

You can combine any and all of these together, eg:

```bash
$ ls m?m?s*_[!0][0-9][0-9].py
```

---

Now let's learn some more common commands

To navigate which directory we are in we use `cd` (<b>c</b>hange <b>d</b>irectory) command:

```bash
$ cd some_directory
```

To get back one level:

```bash
$ cd ..
```

if you do an `ls -al` in a folder you will see both '.' and '..' as directories.  The '.' is the current directory you are in and '..' is its parent.  This is for creating relative paths that make sense.

Or many levels:

```bash
$ cd ../../../../..
```

Or return to the home directory:

```bash
$ cd
```

We can also do this with 

```bash
$ cd ~
```

as `~` is a shortcut to the `HOME` shell variable.  It is useful as it can be used with any command as as part of a path, e.g. `cd ~/documents`.

To get to get to the `ROOT` directory we use

```bash
$ cd /
```

and to go the the directory we were in last, we use

```bash
$ cd -
```

All commands allow "tab completion" for file/directory names so `cd m<\tab>` would match all directories with `m*` and *complete as much as is unique* which is pretty helpful.  When changing directory to something like "My Documents" we need to treat the space as literal otherwise it thinks you've asked it to change into two directories which doesn't make sense.  For this we can either use:

```bash
$ cd "My Documents"
$ cd My\ Documents
```

For this reason you should avoid creating any directories or filenames with spaces in them when working on a Linux system.  

Next we might want to create or destroy files.  To create a file you can use any command that alters a file as generally they will create the file if it does not exist.  `touch` is a common one to use for this as all it does normally is update the files' timestamp. 

```bash
$ touch christmas_list.txt
```

will create a blank file called `christmas_list.txt`. Interestingly, it also lets you edit the access and modification time stamps to be whatever you want, which is helpful if you need to prove you were busy coding when the diamonds went missing.  The syntax is:

```bash
$ touch -d 1999-12-25T01:32:24 christmas_list.txt
```

Deleting files is more specific.  Here we use `rm` (<b>r</b>e<b>m</b>ove), for directories use `mkdir` to create directories and `rmdir` to delete them:

```bash
$ mkdir tmp
$ cd tmp
$ touch testfile.txt
$ cd ..
$ rm tmp/testfile.txt
$ rmdir tmp
```

These all accept globbing, so `rm *.out` removes all files ending in `.out`.  `rm` will also remove empty directories, and with `-r` option (<b>r</b>ecursive) will delete the directory and everything in it.  You can also disable confirmation with `-f` (<b>f</b>orce).  Be \*VERY\* careful with this. `rm -rf *` will remove all files and directories from this directory up, without confirmation.  There is no "Bin" on the command line where files go to while you think about things, **deletions cannot be reversed**. Once they are gone, they are gone forever.  `rm *` will not delete hidden files as `*` will only match non-hidden ones.

We can make copies of files with `cp` (<b>c</b>o<b>p</b>y) where the syntax is `cp file_from file_to`:

```bash
$ touch a.txt
$ cp a.txt b.txt
$ ls -ltr *.txt
```

or just move them with `mv` (<b>m</b>o<b>v</b>e):

```bash
$ mv b.txt c.txt
$ ls -ltr *.txt
```

`mv` is for changing the file's directory or renaming files.  `mv` is much quicker than `cp` as `cp` actually duplicates all the data in a new location, `mv` only changes the name and path (directory it is listed in.  As an aside, directories don't really exist on physical file systems, they are just a tag to help people keep track of them and to aid display so `mv` never actually moves anything).  `mv` can move multiple files using wildcards in the first argument provided the second argument is a destination directory. It cannot rename multiple files via syntax like: `mv *.csv *.txt` which you may think can change the extension of all csv files.

 To rename multiple files there **sometimes** is the command `rename` (it's non-standard so won't be on all distributions, which is a shame as it's handy.  Check with `man rename`) which has the form (note that as it is non-standard this can also change depending on distributions!)

`rename 'old string' 'new string' 'pattern to match files'`

So to change all our `*.txt` files to `*_old.txt`:

```bash
$ rename .txt _old.txt *.txt
$ ls -ltr *.txt
```

*If rename is not present in your distribution you can duplicate it with either a script or on a single line with fancy re-direction.  The command: `find . -name "*.txt" -exec sh -c 'mv "$1" "${1%.txt}.csv"' _ {} \;` uses the the `-exec` or execute option to specify a command to run for each file found; the above changes the extension from ".txt" to ".csv".  We will understand more of this command when we look at scripting later*

Finally when we need to find things we can use `find` to locate files in a directory tree.  The syntax is `find` 'where to look' 'options of which `-name` is always wanted' 'filename with optional wildcards':

```bash
$ find . -name "*.txt"
```

---
**NOTE - Wildcard expansion**

Here is a real "trap for young players".  If you just typed `find *.txt` you would think that the command worked perfectly but it isn't doing what you think.  When you use wildcards on the command line they are expanded **before** the command is run.  So in this case it expands `*.txt` to match all files in the current directory, then finds each of them in turn. The correct version above will search for any file that matches the `"*.txt"` in this folder *and all sub-directories*. The quotes indicate that we do not want the wildcards expanded but passed to the command as is.  However, there is a difference between single and double quotes with `""` meaning we prefer for the wildcards not to be expanded and `''` indicating that they must not be expanded at all.  Backticks \`\` around an expression indicate that it must be expanded before the command is run and is equivilent to using $() around the expression.  The difference can be important.

There is additional complexity for users on macOS or Windows where the behaviour can be a little different as they are not strictly Linux systems. (On my mac the `-name` option protects what follows from being expanded so `find . -name *.txt` produces the correct behaviour, even though accoding to the standard it shouldn't)

---

To simply read a file, to see what is in it, we can use `cat`, `more` or `less`:

```bash
$ cat d.txt
$ more d.txt
$ less d.txt
```

`cat` is good for small files as it reads all of them at once and displays the text.  It's main purpose is actually to con<b>cat</b>enate files (join them together) so as used above it concanenates the file to nothing and pushes the output to the terminal.  `less` and `more` both just do a page at a time and have a lot of options with `-n` for line numbers being the most useful.  `head` and `tail` lets you read from the top or bottom of a file and `tail -f` (<b>f</b>ollow) is useful for tracking output to files your code is writing to without locking them (which can cause code to crash.).  You can open files from the end and scroll upwards with `less +G`

If the files are large and we only want to find some particular section we can use `grep` (**g**lobal search for a **r**egular **e**xpression and **p**rint) to find text in a file, eg: 

```bash
$ grep hello file.txt
```

Will return the lines in `file.txt` which contain the text `hello` anywhere on them.  To use regular expressions you need to add the option -E, which just means <b>E</b>xtended which means it can use regex, **reg**ular **ex**pressions.  

---
**NOTE: Regular Expressions**

It is important to note that regular expression wildcards are **different** to the globbing wildcards we met earlier!!! Now we have the following:
- `.` matches a single character rather than `?`
- [a-z] and standard sets work the same
- `a?`, `a*`, `a+`, mean match 0 or 1 `a`, 0 or more `a`, 1 or more `a` respectively. `a{N}`, `a{N,}` and `a{N,M}` means match N times, N or more times and N to M times respectively.
- `^` and `$` mean it must start at the beginning or end of a line respectively
- `\<` and `/>` matches empty strings before and after
- `.*` gets you the behaviour of `*` from before as it will match any number of `.`, which is any character.

The difference is that the first set of wildcards are for **Globbing** which matches filenames, and are expanded by the shell (by a command called `glob`).  The second set above are for **Regular Expressions** which are for defining search patterns for text, and are expanded by the function.  If you remember the filename vs text search distinction this should help you to avoid confusing them.  

---

Here also meet the importance of quotes. Suppose we have a file called `greeting.txt` which contains the text `hello`. For the following commands we would see:

```bash
$ grep hello greeting.txt     ->  hello
$ grep hello *.txt            ->  hello
$ grep hello "*.txt"          ->  grep: *.txt: No such file or directory 
$ grep hello '*.txt'          ->  grep: *.txt: No such file or directory 
```

grep has several useful options `-A, -B, -C` (note capitalisation) followed by `num` will return `num` lines before, after, or before and after, the match respectively.  This can be very useful for finding uses of functions in your code. `-n` will also print the line numbers.  For example:

```bash
$ grep -n -C 3 'func1' *.py
```

will give you all the uses of `func1` in you python files in the current directory, with the preceding and trailing 3 lines, and give you the line numbers where they occour.

Grep can also search for multiple things at once using `|` which here means "or", eg:

```bash
$ grep -n -C 3 'func1|func2' *.py
```

and multiple files with a glob, or just by listing the files.  Note that with grep you can use both regular expression wildcards and globbing wildcards in the same expression!

Sometimes you input commands by mistake.  While they are running you can exit them using `ctrl-c`.  You may need this if for instance you `grep` something in a folder with an enormous amount of files which could take a very long time to complete. 

## Command history

Up and down arrows allows you navigate through previously entered commands which you can run again with enter. (Note that if you want to "scroll up" in the terminal to see the previous commands output(and the mouse wheel is not working/ available), you (usually) need to hold the shift key while pressing the up/down arrows, otherwise you will only see the history of the commands.) 

To see your command history you can use the built-in shell command `history` which will display a numbered list of all the commands you have entered previously.  You can then retrieve a command using `!num` which will run the command number `num` from history.  If the list of commands is too long you can also "reverse search" your command history it by pressing `CTRL+R` and typing the part of the command you remember.  You can also use the up and down arrows to navigate from the retrieved command to find others.  


## File manipulation
BASH has many commands which are very helpful for file manipulation.  Here we will review the more basic ones but we will come back to this to describe some more advanced tools in subsequent lectures (at least for the DIS students).  The first two are self explanitory: `sort` and `uniq` which sort a files contents and removes duplicates respectivley.  

In linux file extensions (the "ext" in "filename.ext".  These are often hidden in modern systems but are how the computer decides which files each application can open) are optional and up to you to assign for files you create.  Sometimes if you neglect them then you may not be able to open them with the application you desire.  If you hve forgotton what type of file they are you can use the command `file` will try to determine what type of file you are dealing with.  The option `--extension` will suggest what extensions would be suitable for this file type.

There are a number of commands for compressing and bundling files together for transfer.  The first is `tar` which bundles files together.  This can then be compressed with `gzip`.  Alternatively you can just use `zip` which will do both. The first will join the files together then compress them. The second compresses the files then joins them together.  The first achives better compression as it can expliot similarities between files.  The second allows you to etract files individually from the archive which the first does not allow.


Typical use is:
```bash
$ tar -czf file.tar.gz "list of files"
$ tar -xf file.tar.gz
$ zip file.zip "list of files"
$ unzip file.zip
```
where `c` is create, `z` is compress using gzip, `f` means I'm specifiing the output filename, `x` means extract.  `zip` is simpler

Finally we will examine the very important command for comparing files, `diff`.  This takes two files and outputs line by line differences between them.  This is particularly useful for checking what has changed in code files and forms the basis of version control systems.

You use it like this:
```bash
$ diff file1 file2
```
This will produce and output which describes how to change the first file to be identical to the second.

The output will have the following format whenever a change needs to happen:

```bash
"file1 line start","file1line end"{a,c,d}"file2 line start","file2 line end"
> lines in
> file1
---
< lines in
< file2
```
where {a,c,d} means add, change, delete. This is much clearer in examples:

for diff_file1.txt:
```bash
dog
cat
fish

hat
coat
scarf

one
two
```
diff_file2.txt:
```bash
dog
cat
bird

hat
coat

one
two
three
```
Then diff would produce:
```bash
$ diff diff_file1.txt diff_file2.txt
3c3
< fish
---
> bird
7d6
< scarf
10a10
> three
```
So we need to change line 3 of file_one and file_two from "fish" to "bird".  I need to delete "scarf" from line 7 so they sync up at line 3 and I need to add "three" at line 10 (from line 10 in file_two).  You can apply the results of `diff` with the command `patch` which will apply the output of a `diff` to a file.  Here is an example:

```bash
$ diff file1.py file2.py > file.patch
$ patch file1.py file.patch
```

This will update "file1.py" to be identical to "file2.py" which could have be achieved more easily with `cp`.  However you could edit the patch file to only apply partial changes which may be harder to achieve via other methods.

Now let's see some of the more advanced tools:

Firstly we have `cut` which allows you to extract specific columns from text file.  You can specify the delimiter for this or just use specific byte or character positions.  For example, given the tab separated file `data.txt`

```
12:34   cat     1:3     apple
08:12   dog     2:4     pear    
23:59   fish    5:6     banana
```

Then we would have the following
```bash
$ cut -f 1,3 data.txt   (columns 1 and 3)
12:34	1:3
08:12	2:4
23:59	5:6

$ cut -f 1-3 data.txt   (columns 1 to 3)
12:34	cat	1:3
08:12	dog	2:4
23:59	fish	5:6

$ cut -d ':' -f 2 data.txt    (change the delimiter to ":" and select the second column)
34	cat	1
12	dog	2
59	fish	5

$ cut -b 2,4,7,10 data.txt  (or -c, as bytes and characters are the same unless the encoding has multibyte characters)
23c	
81d	
35fh
```

Note: you can't reverse the order of columns, `cut -f 3,1 data.txt` produced the same output as `cut -f 1,3 data.txt`.

This links to similar commands `paste` and `join` which combine files.  First, `paste` combines files as columns. So if we have the two files `numbers.txt` and `letters.txt`, which just list the first 5 numbers or letters respectively, the paste would merge them:

```bash
$ paste numbers.txt letters.txt
1	a
2	b
3	c
4	d
5	e

$ paste -d ':' numbers.txt letters.txt
1:a
2:b
3:c
4:d
5:e
```

This can be used to reverse columns using cut:

```bash
$ paste <(cut -f 3 data.txt) <(cut -f 1 data.txt)
1:3	12:34
2:4	08:12
5:6	23:59
```

`join` merges two tables using a specific key field.  Suppose we have the four files

```
file1.txt   file2.txt   file3.txt   file4.txt
---         ---         ---         ---
1	cat     1	green   1	house   meat	24	dog
2	dog     2	blue    1	cave    meat	12	cat
3	fish    3	red     2	stream  weed	89	fish
4	bat     4	yellow  3	bush    berries	2	bat
5	fox     5	grey                rubbish	76	fox
```

then we could join them as follows:

```bash
$ join file1.txt file2.txt
1 cat green
2 dog blue
3 fish red
4 bat yellow
5 fox grey

$ join file3.txt file2.txt
1 house green
1 cave green
2 stream blue
3 bush red

$ join -1 2 -2 3 -o '1.1 2.2 1.2 2.1' file1.txt file4.txt
2 24 dog meat
3 89 fish weed
4 2 bat berries
5 76 fox rubbish
```

The first is a simple join on the first column, the second shows that it can cope with repeated entries in one file.  The third shows how to use `-1` and `-2` to specify the column in each file to use for the match and how to use the `-o` option to specify the order columns to use in the output.  The third has an additional issue which is that `join` assumes that files are sorted before joining. As the "cat" and "dog" records are swapped, the "cat" record is lost in the join.  To fix this we can do:

```bash
$ join -1 2 -2 3 -o '1.1 2.2 1.2 2.1' <(sort -k 2 file1.txt) <(sort -k 3 file4.txt) | sort -k 1
1 12 cat meat
2 24 dog meat
3 89 fish weed
4 2 bat berries
5 76 fox rubbish
```

where we are sorting the input to `join` on the fly, then sorting the output from `join` to get the original ordering by number
Note that when working with tabulated date we can display it nicely using the `column` command which can be useful for viewing data with odd delimiters, e.g:

```bash
$ column -t -s ':' data.txt
12  34	cat	1   3	apple
08  12	dog	2   4	pear    
23  59	fish	5  6	banana
```

## Redirection

Now that we have seen some basic commands we can learn one of the more powerful aspects of bash, which is redirection.  Redirection lets us pass the output of one command to another. This lets us combine commands to perform some quite sophisticated things.  

We have a selection of tools that let us redirect the input, `STDIN (0)`, and output, `STDOUT (1)` and `STDERR (2)`, of a command.

```
STDIN   -->  | COMMAND |  --> STDOUT
             |         |  --> STDERR
```


Firstly we can redirect `STDOUT` from one command to a file or the contents of a file to a command using `>` and `<` 

```bash
$ ls -l > output.txt
```

Will list our directory, and write it to a file called `output.txt`, which it will create it if it does not exist (so `> somefile.txt` works the same as `touch somefile.txt`).  We can also append to the end of an existing file using `>>`.

```bash
$ grep 'func' code.py >> output
```

`>` redirects only `STDOUT` to the file and passes `STDERR` to be displayed in the terminal.  To capture the errors we need to use `2>` (as `2` means `STDERR`), eg:

```bash
$ ls test.txt 2> errors.txt
```

If we want to capture both `STDOUT` and `STDERR` we can either `&>` or combine the ouput:

```bash
$ ls *.txt &> output.txt
$ ls *.txt >output.txt 2>&1
```

Where the first combines the two and writes them to `output.txt` and the second directs the `STDOUT` to `output.txt` then directs `STDERR` to wherever `STDOUT` points.  The `&` in front of the `1` makes it mean `STDOUT`, rather than a file called "1".  This expansion is done **before** the command is run so it works the same.  This can be confusing, so let's look at the second case step by step.

```
        Starting location   After > output.txt  After 2>&1
---

STDOUT  /dev/tty            ./output.txt        ./output.txt
STDERR  /dev/tty            /dev/tty            ./output.txt
```

where `/dev/tty` is just a special location which means the terminal.  The other special location is `/dev/null` which delete the output. If we did the reverse `ls *.txt 2>&1 >output.txt` we would have:

```
        Starting location   After 2>&1      >output.txt
---

STDOUT  /dev/tty (1)        /dev/tty (1)    ./output.txt
STDERR  /dev/tty (2)        /dev/tty (1)    /dev/tty (1)
```

Where we have used numbers in brackets to differentiate the identical `/dev/tty` locations.

We can also do the reverse and pass the contents of the file to `STDIN` using `<`

```bash
$ grep hello < some_file.txt
```

which will search for `hello` in the file `some_file.txt` (you can do this without the `<` and it will still work fine).  Why would you do this as it seems unnecessary?  There is a subtle difference between the two which is that `<` anonymises the input.  This means that if we compare the two methods:

```bash
$ wc -l dog.txt     produces:       1 dog.txt
$ wc -l < dog.txt   produces:       1
```

so second removed the default printing of the filename from `wc` (which does a **w**ord **c**ount).  There are also situations where piping the input to commands is simpler. 


The next key action we can do is to redirect the output of one command to another.  This is called **pipeing** and is done with `|` for example.

```bash
$ ls -l | grep Jan > January_Files.txt
```

Will list all files in our directory in long format, then use grep to select all those which were last edited in January, then put the output in a file called January_Files.txt.  This is super useful (particularly with grep to search output) and can be used to do a wide range of things.

```bash
$ history|grep "grep"       (find all grep commands you have used)
$ head -n 100 file.txt | tail -n 20 > lines_81_to_100.txt
$ ls -la | more  (allows us to look at the output of `ls` one page at a time)
```

You can chain together as may command as you want:

```bash
cat file.txt | sort | uniq | head -n 3 > first_three.txt
```

Which uses `cat` to load the contents of the text file into memory then `sort`s it alphabetically, removed duplicates with `uniq`, and selects the first three lines to output to a file.
