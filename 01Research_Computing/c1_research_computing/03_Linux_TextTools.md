# Linux Text Tools*

Linux has some powerful tools for managing text files.  Here we will investigate how you can use them to automate some common tasks in your research.

## File Editing
As we saw before `BASH` has some incredibly powerful tools for working with files and it will generally give the best performance of any approach.

We have already met some of the commands for working with text files: `grep`, `sort`, `uniq`, `wc`, `head`, `tail`, `cat`, `cut`, `paste`, `join`, and `column` which are all fairly self explanatory and do everything you would expect (but do check out the `man` pages for them as they have many options).

More advanced tools are available, but they can be tricky to use.  Here we will review three commands which are very powerful, very fast, and very hard to master.  You can achive the same using python scripts but for larger data or some specific tasks these tools can be a life-saver.  They are best used to automate the editing of the contents of files using. 

The simplest of the three is `tr` which just **tr**anslates characters (or more accurately transliterates).  It works on characters, swapping matched ones with suggested replacements.  It understands all the standard character sets (`POSIX`) which allows for some useful options. Here are some examples:

```bash
$ tr 'a' 'b' <filename.txt                  (replaces any 'a' characters with 'b')
$ tr "[a-z]" "[A-Z]" <filename.txt          (lower to upper case)
$ tr "[:lower:]" "[:upper:]" <filename.txt  (same using POSIX)
$ tr '{}' '()' <filename.txt                (change brackets)
$ tr ',' '\t' <filename.txt                 (change commas to tabs)
```

Note:  there are two special characters which are difficult to type so they have symbolic representations, `tab` -> `\t` and `new line` -> `\n`

You can use `-s` to '**s**queezes' multiple of the same characters into a single one *after* substitution. So the following converts multiple spaces into single ones by replacing spaces with spaces *then* the `-s` option squeezes them down.

```bash
$ tr -s ' ' ' ' <filename.txt
```
This is really useful if you have fixed width data and want to change it to delimited data, which can be hard to do otherwise.

You can also use it to **d**elete characters with `-d` and **c**omplement (as in match all but) the selection with `-c`

```bash
$ tr -d "[:digit:]" < filename.txt      (removes all digits)
$ tr -cd "[:digit:]" < filename.txt     (removes everything that is not a digit)
```
The other great feature is that these utilities accept globbing, so you can process large numbers of files very quickly.

---

Now we more onto the big beasts of file editing: `sed` and `awk`.  These are more 'general purpose text processing utilities' rather than commands, in fact they often described as a whole scripting languages of there own.  Here we will introduce you to the basics of what they can do and leave you to explore the full possibilities on your own.

### SED
First let's look at `sed` which is a **s**tream **ed**itor.  This processes files line by line, and performs actions on each one.  This may sound limited but the scope of what it can do is large (people have written programmes that solve sudoku's using only sed).  We will look at some of the most common uses soon, but before then we will need to describe how it works and introduce you to the functions availble to it.

Sed has 4 "spaces" that it uses to process files.  They are the **input** space, the **pattern** space, the **hold** space, and the **output** space.  The basic usage looks like this:
```bash
$ sed [options] 'commands' <[filename] 
```
When sed is run the default behaviour is this:
- read the first line of the **input** space (the file "filename" in the above) and place it in the **pattern** space
- apply all the commands specified inside the single quotes to it
- output the **pattern** space to **output** (the terminal in the example above)
- read the next line from the input space into the **pattern** space ...

This means that if you run `sed <file.txt` it will do the exact same as `cat file.txt`, read the file and output it to terminal.  The difference is that `cat` will read the whole file at once, where as `sed` reads each line into the pattern space, does nothing, then outputs the pattern space to terminal.  Note the output to terminal at the end of the command can be suppressed with the `-n` option so `sed -n <file.txt` will produce nothing

Let's now learn about some of the commands available to us.  To use a command we simply include it in single quotes; to define multiple commands we just add then with `;` between them, inside the same set of single quotes.  Here are the simplest commands:
- `d`/`D` *D*elete the pattern space and go to next cycle / Delete the *first line* of the pattern space and go to next cycle
- `p`/`P` *P*rint the pattern space to output / Print the *first line* of the pattern space to output
- `n`/`N` Write the pattern space to output and replace the pattern space with the *N*ext line from input / *Append* the Next line to the pattern space

So suppose we have the file quote.txt:
```
Debugging is twice as hard as writing the code in the first place. 
Therefore, if you write the code as cleverly as possible, 
you are, by definition, not smart enough to debug it.
```

If we did `sed 'd' <quote.txt` we would get nothing as each line is loaded then deleted. `sed 'p' <quote.txt` produces the quote with each line repeated twice (as it loads the line, prints the pattern space, reached the end of commands so prints the pattern space and reads the next line in).  `sed 'n' <quote.txt` just outputs the quote (reads line 1 to pattern space, `n` causes us to print the pattern space out then load the 2nd line to the pattern space, commands end so we print the pattern space out and load the third line which is output by `n` then reach the EOF).  Hence, if we did `sed 'n;d' <quote.txt` we would only get odd lines back.

These are not so useful so far.  However, we can modify commands by supplying a pattern in slashes. Then the command is only run when there is a match.  For example `sed -n '/write/p' <quote.txt` will act as `grep` only returning the lines with the pattern "write" in it.  The pattern is a `REGEX` so all wildcards mentioned for grep work here.  the command `sed -n '/w.*e/p' <quote.txt ` will match both "twice ... place" and "write .... possible" and print both lines ***as REGEX are greedy so match the largest extent possible***.  Matches can be inverted using `!`, eg `sed -n '/write/!p' <quote.txt` prints all lines which don't match (which is the same as `sed '/write/d' <quote.txt`).

Now onto some more useful commands.  First is `s` which **s**ubstitutes patterns.  The format is: `s/REGEX/replacement/flags`.  The simplest example is word replacement, eg:
```bash
$ sed 's/code/story/' < quote.txt
Debugging is twice as hard as writing the story in the first place. 
Therefore, if you write the story as cleverly as possible, 
you are, by definition, not smart enough to debug it.
```

It defaults to only substituting the first match in each line, use the flags `g` to make it **g**lobal to match all or `N` to match the first **N** matches on each line, this makes `sed s/find/replace/g` a global find and replace.  You can use the matched string in the replacement using the special character `&`
```bash
$ sed 's/w.*e/**&**/' < quote.txt
Debugging is t**wice as hard as writing the code in the first place**. 
Therefore, if you **write the code as cleverly as possible**, 
you are, by definition, not smart enough to debug it.
```
which proves the earlier point about matching being greedy.  

Note: to not be greedy in this case we need to be a little tricky:
```bash
$ sed 's/w[^e]*e/**&**/' < quote.txt 
Debugging is t**wice** as hard as writing the code in the first place. 
Therefore, if you **write** the code as cleverly as possible, 
you are, by definition, not smart enough to debug it.
```

Let's step through the `REGEX` together: begins with `w` which matches "w", then [^e] matches anything that is not an "e", the following `*` means any number of "not e"s then the final `e` means we end on a "e".  We can get sophisticated by using brackets and allowing **E**xtended `REGEX` using `-E` 
```bash
$ sed -E 's/(w)[^e]*(e)/\1***\2/' < quote.txt 
Debugging is tw***e as hard as writing the code in the first place. 
Therefore, if you w***e the code as cleverly as possible, 
you are, by definition, not smart enough to debug it.
```
Now we match the `w` (with the brackets assigning this to `\1`), any number of not "e"s with `[^e]*`, then the final `e` (with the brackets assigning this to `\2`).  We can then replace the middle with "***" using `\1***\2`.

The next command is `y` (which doesn't seem to stand for anything).  This is like `s` but for characters (making it like `tr`).  It will replace all instances of a character with another character, you can specify multiple and it will pair them up in order:
```bash
$ sed -E 'y/abc/123/' < quote.txt
De2ugging is twi3e 1s h1rd 1s writing the 3ode in the first pl13e. 
Therefore, if you write the 3ode 1s 3leverly 1s possi2le, 
you 1re, 2y definition, not sm1rt enough to de2ug it.
```
so has swapped `a->1, b->2, c->3`.  `tr` is more powerful as it understands POSIX character classes but `y` does not.  This means converting case using sed involves expressions like (the somewhat entertaining): `sed y/abcdefghijklmnopqrstuvwxyz/ABCDEFGHIJKLMNOPQRSTUVWXYZ/`

Note: sed accepts ranges for lines to work on.  This is done before the command in the single quotes with the line numbers wanted.  It looks like this:
- `sed '1d' <input.txt`  (delete line 1)
- `sed '1,3d' <input.txt`  (delete lines 1 to 3)
- `sed '3,+5d' <input.txt`  (delete line 3 and next 5 lines)
- `sed '/cat/,/dog/d' <input.txt`  (delete all lines between the line containing cat until the line containing dog, inclusive)
- `sed '!1d' <input.txt`  (delete everything except line 1)
- `sed '$d' <input.txt`  (delete the last line)

Now let's consider some more advanced commands in for sed which manage the **hold** space (which we have not used until now):
- `h`/`H` replace the contents of the **h**old space with the pattern space / append the pattern space to the hold space
- `g`/`G` replace the contents of the pattern space with the hold space (**g**et) / append the hold space to the pattern space
- `x` e**x**change the pattern space and the hold space

One key point to note is that the hold space starts with ***one newline character in it***.  You need to keep this in mind as it can lead to some possibly unexpected behaviour. For instance `sed 'G' <quote.txt` will insert blank lines in between each line as it: reads in a line, appends hold (which is a new line), commands end so prints pattern space and reads next line.

On their own these do not seem very useful but the addition of a hold space allows us to do much more sophisticated things.  Using the hold space we can reverse the order of a file with
```bash
$ sed '1!G;h;$!d' <quote.txt
```
This will:
- load line1 into pattern
- `1!G` is ignored as we are on line 1 (remember 1! is the range "not 1")
- `h` copy line1 in pattern to hold
- `$!d` delete pattern, go to next cycle
- load line 2 into pattern
- `1!G` append hold to pattern so pattern now has "line2 \n line1"
- `h` copy "line2 \n line1" in pattern to hold
- `$!d` delete pattern, go to next cycle
- load line 3 into pattern
- `1!G` append hold to pattern so pattern now has "line3 \n line2 \n line1"
- `h` copy "line3 \n line2 \n line1" in pattern to hold
- `$!d` no delete as last line
- end of commands, print pattern to output

However the hold space is mostly useful for things like printing the line preceding a matched one.  This is normally tricky as the line has already been processed and you can't go back.  Here we can remember the previous line with:
```bash
$ sed -n '/error/{x;p;x;};h' <output.txt
```
where the `{}` are there to let `sed` know that the commands `x;p;x;` (last ; is only required on mac systems for some reason) are all attached to the `REGEX` "error".  Here every line goes in hold until a match when it is swapped to pattern, printed and then swapped back.

Now we have the some less used commands:
- `=` add line numbers followed by a new line character to output
- `r file` read in "file" and output just before reading next line
- `w file` write pattern space to "file"

`=` can be done more easily with other commands and the new line character is annoying.  If you use it you get:
```bash
$ sed '=' <quote.txt
1
Debugging is twice as hard as writing the code in the first place. 
2
Therefore, if you write the code as cleverly as possible, 
3
you are, by definition, not smart enough to debug it.
```
which you then have to fix with another `sed`:
```bash
$ sed '=' <quote.txt | sed 'N;s/\n/ /'
1 Debugging is twice as hard as writing the code in the first place. 
2 Therefore, if you write the code as cleverly as possible, 
3 you are, by definition, not smart enough to debug it.
```

Finally there are the commands ***only for very experts***. They work like the old `GOTO` commands in early FORTRAN code (i.e. from the 70's).  The reason you will not have heard of `GOTO` is that it is a fantastically confusing programming practice which makes you code almost impossible to follow.  As a result it has been removed from almost all modern languages except where backwards compatibility is required.  Here are the commands:
- `:label` define a label at this point of the script
- `blabel` branch (GOTO) the location "label" in script, or if there is no label start next cycle 
- `tlabel` branch (GOTO) the location "label" in script *if any successful substitutions have occoured this cycle* (`T` is the reverse)
- `#` this line is a comment, as in ignored

This make sed a full programming language but it is not for the faint hearted.  Here is the simplest example I could find:
```bash
$ sed '/a/{s/a/*/
> : loop
> n
> b loop
> }' <quote.txt
Debugging is twice *s hard as writing the code in the first place. 
Therefore, if you write the code as cleverly as possible, 
you are, by definition, not smart enough to debug it.
```
This looks for "a" then replaces it with "*" then we use the loop to just print the rest of the file.  This allows us to only substitute the first instance of "a" in the file.  You have to enter the commands on multiple lines as the `;` doesn't work here (on mac at least, Linux is probably OK). We need an actual `new line` instead.  This is because you would pretty much always use this in a script rather than a command line.  Here you would create a file with the commands:
```
/a/{s/a/*/
: loop
n
b loop
}
```
and run it with the `f` option
```bash
sed -f command_file.sed < quote.txt
```

This command could be updated to have 
```
/a/{s/a/*/
: loop
n
1,2b loop
}
```
So it would do 2 lines then look for another substitution.  This has turned it into something like a **for**-loop (for i=1 to 2 do ..).  Combined with the /a/{} which acts as an **if**, we get our full programming language.

Now let's move onto `awk`

### AWK
While `tr` deals with characters, and `sed` deals with lines, `awk` deals with **records** and **fields**.  It is very powerful for automating file editing, and like `sed` is really a scripting language but `awk` is much more explicit about it.  The name `awk` isn't short for anything, it is just a concatenation of the first letter of its authors surnames: Aho, Weinberger, Kernighan and is was originally written in 1977 and released publicly in 1989 so it's pretty old.  Why would you use such an old language when you could do it all in `pandas` in `python`?  Simply `awk` will be much faster and more flexible than any formatting tools available in `pandas`.   Often you can do very complex transformations using single line commands, it is easy to automate with scripts, and it is available on every machine with bash so is very portable.  Also with globbing you can use it to act on a large number of files simultaneously

The basic operation `awk` performs is to read a line of a file, parse it into fields using a given delimiter, perform actions on the line, move to the next line.  The default syntax is very similar to `sed`

```bash
$ awk [options] 'commands' [filenames] 
```

Like `sed` the commands are enclosed in single quotes and take the same form of `/pattern/ {action}`.  The actions in `awk` are done with functions rather than letter based commands and `awk` also relies on many implicit variables.  Let's look at the simplest examples with the variables `$num` and function `print`

Suppose we have "file4.txt" from earlier:

```bash
$ cat file4.txt
meat	24	dog
meat	12	cat
weed	89	fish
berries	2	bat
rubbish	76	fox
```

Then we can use `awk` to select just the last column

```bash
$ awk '{print $3}' file4.txt
dog
cat
fish
bat
fox
```
here we have no `/pattern/` so we match every line and we `print` the third column `$3`.  The standard field delimiter is "white space" so spaces or tabs.  This can be changed using the `-F` option, i.e. `$awk -F ":" ...` changes it to ":".  You can specify anything and can have multiple using either "a|b" or "[ab]" which will use either "a" or "b" as the delimiter.   We can use awk to easily reorder the columns as we like
```bash
$ awk '{print $3,$1,$2}' file4.txt
dog meat 24
cat meat 12
fish weed 89
bat berries 2
fox rubbish 76
```
We can add a pattern to match,
```bash
$ awk '/a/{print $0}' file4.txt
meat	24	dog
meat	12	cat
berries	2	bat
```
which prints all lines containing "a" ($0 means the whole line).  We can change the format of our output by switching `print` for `printf` which takes format specifiers:
```bash
$ awk '{printf("The number is %d\n",$2)}' file4.txt
The number is 24
The number is 12
The number is 89
The number is 2
The number is 76
```
Here the command `printf` outputs the string in double quotes substituting the fields that follow after the comma, `$2` here, into the space denoted by `%d`.  `%d` is a format specifier meaning `integer` (or **d**ecimal).  The list of most used ones are (there are also several dealing with hexadecimal or octal representations but I've never found a use for them):
- `%c` single **c**haracter
- `%s` **s**tring
- `%d` (or `%i`) **d**ecimal notation (**i**nteger)
- `%f` **f**loating point
- `%e` **e**xponent notation

Here is an example:
```bash
$ awk '{printf("%%d=%d\t%%f=%.3f\t%%e=%.3e\n",$2,$2,$2)}' file4.txt
%d=24	%f=24.000	%e=2.400e+01
%d=12	%f=12.000	%e=1.200e+01
%d=89	%f=89.000	%e=8.900e+01
%d=2	%f=2.000	%e=2.000e+00
%d=76	%f=76.000	%e=7.600e+01
```
Parsing this: `%%d=` gives "%d=" as the `%` escapes the following one, `%d` matches the first argument, `$2`, and prints it in decimal notation, `\t` prints a `tab`, `%%f=` prints "%f=", `%.3f` matches the second `$2` and prints the number in floating point notation with 3 decimal places, `\t%%e=` prints another `tab` followed by "%e=", `%.3e` matches the third `$2` and prints the number in engineering notation with three decimal places and finally `\n` prints a newline character.  This command is identical to that in `C` (which is what `awk` is written in) so should be familiar to anyone who has used that language.  This command is very useful for reformatting output files into more useful forms (like that needed for a latex table to put in a paper).

While we are on the subject of numbers we have access to many common mathematical functions from C in `awk` like `atan2`, `cos`, `exp`, `log`, `sin`, and `sqrt` and operators: `+` `-` `*` `/` `%` `^` (where the last two are "modulo" and "power") so we can do:
```bash
$ awk '{printf("mod 6:%d, cube:%d, sqrt:%f\n",$2%6,$2^3,sqrt($2))}' file4.txt
mod 6:0, cube:13824, sqrt:4.898979
mod 6:0, cube:1728, sqrt:3.464102
mod 6:5, cube:704969, sqrt:9.433981
mod 6:2, cube:8, sqrt:1.414214
mod 6:4, cube:438976, sqrt:8.717798
```
We can also compute averages
```bash
$ awk '{ sum += $2 } END { if (NR > 0) print sum / NR }' file4.txt
40.6
```
Here we have introduced several new concepts. We have created a **variable** `sum` and used `+=`, which means "add to itself" and is equivalent to `sum = sum + $2`, to sum the values.  We have then used the `END` **special pattern** to indicate that we should run the following commands once the file has ended, a **conditional** statement `IF` to test for empty files to avoid divide by zero errors, and the `NR` **implicit variable** "number of current row" which is the total number of rows as we have finished reading the file.  Let us look at each of these concepts in turn:

- **variables** are easy.  To create them you just use them and they are initialised to 0 by default, no `$` is required to access them.
- There are only 4 **special patterns**: `BEGIN`, `END`, `BEGINFILE`, `ENDFILE`.  These specify actions to be taken before or after all commands or before or after commands *for each file*.  The second set allow for the case where multiple files have been passed to `awk` either explicitly or via a filename "glob" 
- **conditionals** to be tested by IF (either explicitly, or implicitly just by putting them before the command brackets) cover all that you would expect.  You have already met `/pattern/` which tests if the line "contains" pattern.  The contains operator can be explicitly implemented using `~`, eg: `$ awk '$3~/a/{print $0}' file4.txt` which tests if `$3` *contains* "a".  Others are the usual suspects: `>`, `>=`, `<`, `<=`, `==`, `!=`.  We can also test conditionals (or more accurately "booleans") using the compact (but less intelligible) ternary operator `boolean ? statement1 : statement2` which tests `boolean` and does `statement1` if true, and `statement2` if false.
- **implicit variables** are just variables defined as standard in `awk`.  They cover most things you would be interested in and can be found in `man awk` with sensible descriptions.  Common ones are `NR` for number of the current record that is read (`FNR` is the version for each file), `NF` is the number of fields, `FS` and `RS` are **f**ield and **r**ecord **s**eparators respectively (`OFS` and `ORS` are the versions for output which I seldom use as I prefer `printf` to specify things exactly), `RSTART` and `RLENGTH` are the start position and length of matched strings (as returned by the function `match`)

Here is is helpful just to see of examples of them in action:
```bash
$ awk '{print $2+previous; previous=$2}'    (rolling sum of last two values)
$ awk '{print $(NF-1)}'             (print the second to last field)
$ awk '{if($2>50) print $0}'        (print lines where 'field 2' is larger than 50)
```
Where in the first line we have specified two commands using the `;` between them.  Alternatively you can just have `{}` for each and the commands will be executed sequentially. You can create more complicated commands like:
```bash
$ awk 'BEGIN { printf("\\begin{table}[ht]\n\\centering\n\\begin{tabular}{c c c}\n\\hline\\hline\n")} {printf("%s & %d & %s \\\\ \n",$1,$2,$3)} END{printf("\\hline\n\\end{tabular}\n\\caption{contents of %s}\n\\label{table:%s}\n\\end{table}\n",FILENAME,FILENAME)}' file4.txt

\begin{table}[ht]
\centering
\begin{tabular}{c c c}
\hline\hline
meat & 24 & dog \\ 
meat & 12 & cat \\ 
weed & 89 & fish \\ 
berries & 2 & bat \\ 
rubbish & 76 & fox \\ 
\hline
\end{tabular}
\caption{contents of file4.txt}
\label{table:file4.txt}
\end{table}
```
which produces your file content in a form that can be copied directly into LaTeX as a table.  For longer commands like this you are better to save the commands in files and input them to awk using the `-f` option just like we did with sed.  `awk` is a full scripting language with `if`,`while`,`for`,`do` constructs and a large number of internal functions so you can really code up almost anything you want to.

`awk` even supports ***associative arrays***, i.e. ones where the indices are just labels (also called "dictionary" in python, or "map" in C++).  The following uses this to count how many animals eat each type of food in "file4.txt"
```bash
$ awk '{food[$1] +=1} END {for (item in food) printf("Food \"%s\" is eaten by %d animals\n",item,food[item]) }' file4.txt
Food "meat" is eaten by 2 animals
Food "weed" is eaten by 1 animals
Food "berries" is eaten by 1 animals
Food "rubbish" is eaten by 1 animals
```
Note the syntax of the `for` loop which is only for arrays (normal use is `for(start cond.,end cond., increment)`). ()

Unlike `sed` where I can cover all the commands pretty well, `awk` just goes on and on.  Here is a link to a 17 chapter book (roughly 827 pages) on it for the comprehensive introduction: https://www.gnu.org/software/gawk/manual/gawk.html.  I will leave you here as the above is enough for most things except the very specialist (which you can google!). The point is that if you have to process text files as part of your research `tr`,`sed`, and `awk` provide a powerful way to process these very quickly and portably.  I find them very useful for processing output files to prepare results for plotting or for presenting in papers which can be easily automated and added to batch scripts so they run automatically.

There are also several commands for reformatting files: `encode`, `decode`, `enscript`, `groff` which I will let you explore on your own as they are less likely to be relevant to research tasks.

### Exercise
First try the examples listed above using the files in `Linux_Resources/Applications`
Use `tr` to convert quote.txt to:
1. Uppercase.
2. Remove all vowels.

Use `sed` to:

3. Add currency symbol before each number in file4.txt.
4. Add "**" before and after the word twice in quote.txt.

Use `awk` to 

5. Make a tab seperated list of the application number, first name, and last name of the applications in the folder `Applications` that you could paste into a spreadsheet (I used this all the time to process your applications!).
