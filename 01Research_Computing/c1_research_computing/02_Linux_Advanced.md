# Advanced Linux Terminal
This material was covered by Phillip Blakely but here is my old version in case it is of interest.


The linux terminal is primarily useful for managing the running of your code, either locally or on remote computing resources.   In this lesson we will cover how to submit and manage jobs from the command line and how to control our computing enviroment.

## Mangaging processes

To submit a job on the command line you just need to pass your script to an interpreter.  Here we used the command structure:

```bash
$ python file.py 
```

Here we specify the **interpreter** to read the code, python, which is contained in "file.py" and convert it to instructions for the computer to carry out.  This is what we are doing in the terminal, but here we don't need to specify the interpreter as it defaults to `bash`.

Often your code could run for a while, and you don't want to have to leave the terminal hanging, so you can specify for the code to run in the **background** by appending `&` at the end.  For example:
```bash
$ sleep 10 &
```
This will create a job that `sleeps` (does nothing) for 10 seconds then returns,  Adding the `&` makes it return control of the terminal immediatly, leaving the process to run in the background instead.  When you do this you are given the message:
```bash
$ sleep 10 &
[1] 84144
```
Where the `[1]` is the "job id" (or jobID) and `84144` is the process identification number (or PID).

Now that your processes are running in the background you need to know when they are complete

List all processes you control:
```bash
$ ps
```

List all processes on the system with all info:
```bash
$ ps -elf
```

We can also open an interactive live picture:
```bash
top
```

This has many options with some of the more useful being `-o` which sorts it by any column but `mem`, `user`, `time` and `cpu` (default) are useful and `-user me123` to display only one user.  These options can be on the command line or while in the top window itself

When you start processes you can do so in the background with `jobscript &` then check them with the command `jobs`. Then `bg` sends the job to the background and `fg` sends it to the foreground.

```bash
jobs -l
sleep 30 &
sleep 20 &
sleep 10 &
jobs -l
fg 3
```

In order to change the status of the jobs you can use the `kill` command:

```bash
jobs -l
sleep 300 &
sleep 200 &
sleep 100 &
kill -SIGSTOP %1
kill -SIGTERM %2
kill -SIGKILL %3
jobs -l
kill -SIGCONT %1
jobs -l
kill -SIGTERM %1
```

The option `-SIGSTOP` means pause the job, `-SIGCONT` restarts it (in the background so this is equivalent to `bg`, you can change it to the foreground, if that's were it was, this with `fg`).  `-SIGTERM` attempts a clean exit so is good for applications (as they get a change to save your data etc..). `-SIGKILL` kills the process no matter what.  These all have numeric shorthands `-9` for `-SIGKILL`, `-15` for `-SIGTERM`.   The other two are system dependent so one of `-17`,`-19`,`-23` for `-SIGSTOP` and `-19`,`-18`,`-25` for `-SIGCONT`.  The most important is 

```bash
kill -9 PID
```
Which can be used to end problem jobs.

*** add nice

## Remote Computing

### SSH

Once you start writing larger codes that exceed the local resources of you computer or laptop you will have to start working on dedicated machines, which you will likely have to access remotely.  This is done with the command `ssh` (<b>s</b>ecure <b>sh</b>ell) which creates an encripted tunnel to remote machines.  The basic command looks like:

```
$ ssh username@machinename
```

This can be tested for DAMTP and DPMMS users with the command below:

```
$ ssh -X CRSid@ssh.maths.cam.ac.uk
```

Which will then ask for your maths password. This just makes your terminal window act like one on the remote machine.  The `-X` allows '**X** forwarding' so can transfer GUI interfaces between the computers if you start applications.

`ssh` has many options of which some of the most useful are `-C` to allow compression of data which is transfered and:
```bash
$ ssh -J  username1@machinename1 username2@machinename2
```
which will perform a proxy**J**ump so will login to machine2 via machine1.  This is helpful for logging into departmental computing machines via departmental ssh machines from your laptop.

When you login with a password like above there is a risk of the password being intercepted and is succeptable to a brute force attacks.  You should instead use `ssh-key` authentication to connect to remote machines. 

***
**Aside:**
This uses asymetric encryption to connect the machines.  Here you generate two "keys" a public and a private one.  The public one is shared with the machine you are connecting to and the private one remains on your local machine (or thumbdrive).  The public key can be used to encrypt communications but cannot decrypt anything, this can ony be done using the private key.  There are various algorythms for connecting but on a simple level a symmetric encryption key is generated at the server level.  This is encrypted using the public key and passed to the remote machine which can decrypt it using the private key.  Now both machines have a key for symmetric encryption without the key being made visable to anyone.  The private key can be protected with a passphrase so even if it is stolen it cannot be used.  When you connect `ssh` will ask for the passphrase but this is not transmitted to the server so cannot be intercepted.
***

To set this up you need to use the command:
```bash
$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/jamesfergusson/.ssh/id_rsa): /Users/jamesfergusson/.ssh/test
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /Users/jamesfergusson/.ssh/test
Your public key has been saved in /Users/jamesfergusson/.ssh/test.pub
The key fingerprint is:
SHA256:9m+S9EynmNAYLEgyHmBs+osQZFUn2r4etdOYur3gJkY jamesfergusson@lapc-br1-238.maths.private.cam.ac.uk
The key's randomart image is:
+---[RSA 3072]----+
|oo...o .         |
|.=+ + o          |
|=. * o .         |
|o . o . o        |
| o   . oS+       |
|. .E  o.B.o . .  |
|.... + = +.B o   |
|. .oo.= . =.=    |
|  . o=.o.  o.    |
+----[SHA256]-----+
```
You can now see the following in the hidden folder `~/.ssh`
```bash
$ ls -l ~/.ssh/test*
-rw-------  1 jamesfergusson  staff  2700 18 Oct 16:23 /Users/jamesfergusson/.ssh/test
-rw-r--r--  1 jamesfergusson  staff   605 18 Oct 16:23 /Users/jamesfergusson/.ssh/test.pub
```
where `test` is the private key and `test.pub` is the public key. Now you need to copy the public key to the machine you want to login to.  You do this using the command:
```bash
$ ssh-copy-id -i ~/.ssh/test username@machinename
```
which will ask for your password then copy the key to the server and store it in a file called `authorised_keys` file in the servers' `.ssh` folder (or elsewhere depending on configuration).  Now when you login to the machine you use the `-i` option to specify your identity like this:
```bash
$ ssh -i ~/.ssh/test username@machinename
```
and you will be asked for your passphrase to continue, eg:
```bash
$ ssh -i ~/.ssh/test jf334@ssh.maths.cam.ac.uk
Enter passphrase for key '/Users/jamesfergusson/.ssh/test':
Welcome to Ubuntu 20.04.5 LTS (GNU/Linux 5.4.0-128-generic x86_64)

=========================================================================
 Ubuntu 20.04.5 LTS (focal) in Maths
 Host: ssh-serv1, Group: DAMTP/DPMMS/GENERAL/PUB/PUB2021/SLURMNODES/STATS, Kernel: Linux 5.4
 Memory: 7955M, Swap: 0M
 Arch: x86_64, AMD EPYC 7313 16-Core Processor [1 cores]
=========================================================================
Last login: Wed Feb  2 15:42:43 2022 from xxxxxxxxxx.xxxxx.xxxxxx.cam.ac.uk
```
If you find entering the passphrase a pain you have two options, the first is to not enter a passphrase when creating the key.  This creates an "open key" which will connect automatically when you ssh.  This is not advised as anyone who has your private key can access your ssh machines but can be acceptable if you machine it is stored on is secure.  Better is to use an `ssh-agent` which is a helper program that keeps track of user's identity keys and their passphrases and enters them you your behalf.  `ssh-agents are generally started on automatically on login but can be started manually with:
```bash
$ eval `ssh-agent`
```
You simpy have to add your keys to the `ssh-agent` using `ssh-add`:
```bash
$ ssh-add ~/.ssh/test
Enter passphrase for test: 
Identity added: test (xxxxxxx@xxxxxx.xxxx.private.cam.ac.uk)
```
Now when connecting using ssh it will manage your passphrases automatically.  There are a few more ways to improve the situation. Firstly you can improve the security by choosing stronger security when creating the key
```bash
$ ssh-keygen -t rsa -b 4096
$ ssh-keygen -t dsa 
$ ssh-keygen -t ecdsa -b 521
$ ssh-keygen -t ed25519
```
You can also create configuration files which store the details for each machine you want to log into.  You can also store your options for each host in a config file in your `.ssh` directory.  The format is the following:
```bash
$ cat ~/.ssh/config
Host maths
    HostName ssh.maths.cam.ac.uk
    User jf334
    IdentityFile ~/.ssh/test
    ForwardX11 yes
```
with this you can `ssh` to the maths ssh server using:
```bash
$ ssh maths
```
This will then read the config file and log into ssh.maths.cam.ac.uk as jf334 using the key "test" with X forwarding enabled, so it is equivelent to:
```bash
$ ssh -X -i ~/.ssh/test jf334@ssh.maths.cam.ac.uk
```
the passphrse will still be handled by the agent so access will be automatic.  You can also use the config file to manage ProxyJumps using:
```
$ cat ~/.ssh/config
Host *
    User jf334
    IdentityFile ~/.ssh/test
    ForwardX11 yes

Host server1
    HostName server1.cam.ac.uk

Host server2
    HostName server2.cam.ac.uk
    ProxyJump server1
```
where the `*` sets the defaults for all ssh commands then  "server1" gives the name for the server which we are going to use to jump through, and "server2" gives the name for server2 and indicates that we should jump via server1 with the `ProxyJump` option.  A full list of options that you can use is availble here: https://www.ssh.com/academy/ssh/config


### Copying files

Once you have setup `ssh` access you can work on the remote computer just like you were there yourself.  However there may be times that you will want to move files between your computer and the remote machine.  There are two ways to do this:

You can copy the files between the machines with `scp` (<b>s</b>ecure <b>c</b>o<b>p</b>y) or `sftp` (<b>s</b>ecure <b>f</b>ile <b>t</b>ransfer <b>p</b>rotocol).  First `scp` works just like `cp`:

```
scp username@machinename:file.txt /local/directory/.
scp -r username@machinename:/remote/directory /local/directory/
```


`sftp` is a bit different.  Here you login to the remote machine and open an `ftp` window where you move files with `get` and `put`:

```
sftp  username@machinename

get remotefile
put localfile

get remotefile copytonewlocalname
```

Everything we did above regarding agents and config applies equally to `scp` and `sftp` as they both use `ssh` to make the connection.

## Scripting

You should also note that all the commands here can be executed as a script (just a file with a list of commands.  It is often given the extension `.sh` as in `somthing.sh`.  `sh` is an earlier version of `bash` so this is actually a bit misleading.  It's not a requirement so you can do whatever you want but it's nice to have something that tells you what it does in the name).  

First you need to start the file with:

`#!/bin/bash`

This isn't strictly necessary but makes sure your computer knows to interpret the following commands using the `bash` language (what the terminal is using for its `kernel` if any of the above worked.  `kernel` just means 'thing which interprets the commands you type') and after this you can just list commands that you want.  This can fail if `bash` isn't in the `/bin` directory.  Instead you might need:

`#!/usr/local/bin/bash` --  Another place bash sometimes lives

`#!/usr/bin/env bash`    Works if `bash` is in your path

You can in fact put any kernel here for any other scripting language, like for example:

`#!/bin/python`

Back to bash, once you have this line you can write commands just like you were entering them into the terminal.  So an example might be:

```
cd ~code/output
rm -f *.log *.out
```

You would then save this into a file `cleanup.sh`. Then you have to change the file permissions to allow execution ie: `chmod 744 cleanup.sh`.  Then you can run it on the command line with

`./cleanup.sh`
or
`bash cleanup.sh`

This can be helpful for sets of commands you often run together.

### Variables
BASH is actually a fairly powerful programming language on its own.  You have variables:

```
var1=1
echo "var1 = $var1"

str1="Hello"
echo "str1 = $str1"
```

Note the double quotes, single quotes will result in `echo` not expanding the variable and printing the name instead.  Also you can't have any spaces in assignment so `var1 = 1` fails.  

#### Strings
Numeric varibles work as expected but strings are a little trickier to work with. To modify a string variable is a bit tricky.  It is done using some basic commands.  For more sophisiticated tasks you need to use sed/awk (advanced!)

The simple commands are:
```bash
echo "**** Strings ****"
test_string1='abcdefghijklm'
test_string2='nopqrstuvwxyz'
echo ${#test_string1}   #string length
echo "** Substrings"
echo ${test_string1:7} #substring from position 7
echo ${test_string1:7:4} #substring from position 7, for 4 characters
echo "** Substring Removal"
echo ${test_string1#'abc'} #shortest substring removed from front
echo ${test_string1##'abc'} #longest substring removed from front
echo ${test_string1%'klm'} #shortest substring removed from back
echo ${test_string1%%'klm'} #longest substring removed from back
echo "** Replacement"
echo ${test_string1/efg/567} #replacement first match
echo ${test_string1//efg/567} #replacement all matches
echo "** note: to make match at front or back add # or %"
echo "** if no replacement is supplied does deletion"
echo ${test_string1/efg} #deletion
echo "** Joining"
echo $test_string1$test_string2 #joining strings, += also works
```
### Loops
It also has loops which can be implemented in various forms:

```
for i in {1..10}; # {1..10} expands to "1 2 3 4 5 6 7 8 9 10"
do 
    echo "List form:    The iteration number is $i"
done

for (( i = 0; i < 10; i++ )) #C style loop
do
    echo "C style form: The iteration number is $i"
done

i=0
while [ $i -lt 5 ] #Executes until false
do
    echo "while: i is currently $i"
    i=$[$i+1] #Not the lack of spaces around the brackets. This makes it a not a test expression
done

i=5
until [[ $i -eq 10 ]]; #Executes until true
do
    echo "until: i is currently $i"
    i=$((i+1))
done
```

### Conditionals
Conditional expressions are straightforward:

```
if [ "$num" -eq 1 ]; then
    echo "the number is 1"
elif [ "$num" -gt 2 ]; then
    echo "the number is greater than 2"
else
    echo "The number was not 1 and is not more than 2."
fi
```
here `-lt`, `-gt`, `-eq` means "less than", "greater than" and "equal to" respectively.

### Functions
Functions exist but are a bit tricky.  You can make basic funtions with the following format
```bash
function_greet () {
    echo "This script is called $0"
    echo "Hello $1"
}

function_greet "James"

$ ./script.sh
This script is called ./script.sh
Hello James
```
Here `$0` is the name of the script and `{$1,$2,$3...}` are variables passed to the function by listing them after it.

Functions don't return variables as standard (there is a `return` command but this is just for integers to indicate error status), to do this you can use global variables:
```bash
# Global variable return
function_add1 () {
    wrong=$1+$2
    sum=$(($1+$2))
}
function_add1 6 7
echo $wrong
echo $sum
```
Note the requirement to have `$((  ))` for numeric calculations else bash assumes you are working with strings.  Global variables can be dangerous so it is better to use local variables:

```bash
# Local variable return
function_add2 () {
    local sum=$(($1+$2))
    echo $sum
}
answer=$(function_add2 6 7)
echo $answer
```

We don't really have time to go over `bash` properly and it would be best to do so after learning python to get you used to coding first as `bash` isn't always all that clear and is very sensitive to syntax.  I will just mention one last thing which is very useful which is `bash` has `&&` meaning "and" and`||` meaning "or" which help for error trapping.  For the first example `cleanup.sh` we should really have done this:

```
cd ~code/output || exit
rm -f *.log *.out
```
Now the script will `exit` if it can't change into the directory.  Before, if this line failed it would then have just deleted stuff wherever you were which is a bit dangerous.

****
All of the above code is in the file `script.sh` in the directory `Bash` if you want to test it out.
****

Aside: command to replicate the `rename` function if not implemented:

```bash
find . -name "*.txt" -exec sh -c 'mv "$1" "${1%.txt}.csv"' _ {} \;
```
Here we have used the `-exec` option to provide a command to execute for each file found.  Let's work through it bit by bit 
Command Breakdown:
- `'.'` => search path starting at current directory marked by ' . '
- `-name` => set files to find (in this case all files that end with `.txt`)
- `-exec` => execute the following command on every match
- `sh -c` => 'exec' creates an independent shell environment for each match
- `mv "$1" "${1%.txt}.csv"` => **m**o**v**e first variable (denoted by $1), which is the current file name, to new name. Here I do a substring match and delete; so take first var again, $1 and use % to delete `.txt` from the string. The `.csv` then concatenates `.csv` in it's place
- The underscore, `_` is a placeholder for $0, the command
- The `{}` is replaced by each (*.txt) filename found by the find command, and becomes $1 to the sh command.
- `\;` marks the end of the -exec command.  You can also use ';' or ";".

None of the above is eash to create on your own without some significant experence but at least you should better understand google results.
*****

NOTE: editing `bash` scripts on windows adds different new line characters and the code will fail.  This can be fixed with things like the programme `dos2unix`.


## vim
In order to edit text files you can use one of the many excellent text editors available.  However they are not always availble and sometime you cannot connect your editor over ssh so it is useful to know how to use a builtin editor like `vim`.

`vim` is entirely text based with no GUI element or tool tips. This makes it very challenging for new users leading to jokes along the line of:

"I've been using vim for 2 years now.  I opened a file back then and I still haven't worked out how to exit"

or

"The only way to generate truly random string of charaters is to ask a new user to save a file in vim"

However it's not too bad once you get some basic commands 

To launch it, you need to type `vim FILENAME`. This will allow you to view the file (and will create it if it does not exist, you can also just type `vim` then which will open a window which you can save to a file when you finish). To edit it, you need to enter the edit mode by typing `i` (for "insert"). After editing, press the escape key to exit "insert mode". To close the file, you need to type `:q` to exit if you didn't edit anything, `:q!` if you edited and want to discard the changes or `:wq` if you want to save them to the file or `:wq filename` to save to a file.

You can easily learn vim using the very good `vimtutor`.  Just type `vimtutor` on the command line and work through all the lessons (~30mins).  If you can master it then it can be the fastest editor availble but if does take a bit of practice!

## Enviroment

When you log in, `bash` will execute several *script* files:
-   system startup files
-   personal ones in `~/.bash_profile` (login sessions) or `~/.bashrc` (other sessions)
-   edit as you see fit, but be careful: mistakes can lead to inability to log in!

When editing bash.rc or bash.profile **MAKE A BACKUP FIRST!!!**  If you mess it up then you have a way back.

*Environment variables* control how `bash` behaves; most important one is `PATH` list of colon-separated directory names to look, in order, for commands typed in the prompt:

```
$ echo ${PATH}
```

To see all environment variables use `env`:

```
$ env
```

Editing `~/.bashrc` or `~/.bash_profile` is only sensible for things that you need to set up every time you login to a system.  

You can make shortcuts for frequently used commands with `alias`
```bash
alias short='long command'
```
You can use this for anything you want.  The following will tell you the 10 most used commands in your history to give you ideas:
```bash
$ history | awk '{cmd[$2]++} END {for(elem in cmd) {print cmd[elem] " " elem}}' | sort -n -r | head -10
```

Other things are loading modules your code needs.

As an example here is mine for the cosmos supercomputer:

```
# ~/.bashrc.local
# $Id: .bashrc.local,v 1.4 2009/01/26 11:00:13 root Exp $
# $Source: /home/cosmos/template/RCS/.bashrc.local,v $
#
# Add/modify here your custom environment settings

alias cosmos2='msub -q debug2 -I -V -l nodes=1:ppn=1,mem=50gb,walltime=08:00:00 -N debug_session'

module load icomp mpt gsl cfitsio pgplot healpix/3.40-serial-intel-15.0
module load cosmolib python
```

This sets up the shortcut using the `alias` command so when I type `cosmos2` it executes the command in quotes which launches an interactive job in the debugging queue.  Then I load a bunch of modules I need to run my code on the machines. 

You probably shouldn't load modules this way unless you are sure you will always need them (and will not forget they are there).

If you want to set up shortcuts to locations you can create shortcuts for commands like:
```bash
alias godata='cd /my/data/directory'
```
Or instead create links to make them appear somewhere more convenitent.  Here you just need to use:
```bash
$ ln -s /my/data/directory data
```
which will make the directory "data" appear in your home directory and `cd data` will take you to `/my/data/directory`

You can also customise behaviour of the terminal:
```bash
HISTTIMEFORMAT="%F %T " # add time stamps to history
# set up shortcuts for colours
blk='\[\033[01;30m\]'   # Black
red='\[\033[01;31m\]'   # Red
grn='\[\033[01;32m\]'   # Green
ylw='\[\033[01;33m\]'   # Yellow
blu='\[\033[01;34m\]'   # Blue
pur='\[\033[01;35m\]'   # Purple
cyn='\[\033[01;36m\]'   # Cyan
wht='\[\033[01;37m\]'   # White
clr='\[\033[00m\]'      # Reset
# Then use them to customise your prompt which is contained in thje variable PS1
PS1='${debian_chroot:+($debian_chroot)}'${blu}'$(git_branch)'${pur}' \W'${grn}' \$ '${clr}
``` 


## Some fun


Linux console doesn't have to be all boring, for example, by installing `lolcat` and `oneko` packages and making aliases in the `.bashrc` like

```bash
alias pg='ping google.com|lolcat.ruby2.5 -F 0.3'
alias meow='oneko -bg green'
```

you can get the following colorful ping output and a little cat chasing your cursor:

![](Plots/screenshot.png)

## Further Reading

This should be enough to get you started but there is plenty more.  Here are the notes on the university information service course on the unix terminal:
https://help.uis.cam.ac.uk/service/help-support/training/downloads/course-files/programming-student-files/unix-cli/unix-cli-files/working-copy-unixcli.pdf.

For `bash` scripting here is a link to a free 100 page book which is worth a skim for people who want to know more: https://books.goalkicker.com/BashBook/.  

Or consult the manual:
https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html

Finally here is a list of all commands available in `bash`
https://courses.cs.washington.edu/courses/cse391/17sp/bash.html

Otherwise, as always in coding, google is your friend.

## Exercises
1. Try the process management commands above line by line to see what happens
2. If you have access to a remote machine set up ssh-pass-keys and ssh-agents to automate logins.
3. Copy a file back to your direcotry from a remote machine.
4. Make a script which takes a number and creates a triangle of dots. eg
```bash
$ ./script.sh 5
.
..
...
....
.....
```
5. create an alias for the command `history | awk '{cmd[$2]++} END {for(elem in cmd) {print cmd[elem] " " elem}}' | sort -n -r | head -10` and try it out.
