### Exercise for 01_Linux_Basics
0. Make sure you can open a terminal.
    - Linux -> easy
    - Mac -> f4 and type "terminal"
    - Windows -> activate the Linux sub-system (https://learn.microsoft.com/en-us/windows/wsl/install)

1. Make a directory called tmp and change into it

2. Create a file test.txt

3. Copy it to test2.txt then rename test.txt to test1.txt

4. Delete the files, then delete the directory

For the following, download the `Bash` folder from the moodle site

5. Write a single line command that finds all files for the "DummyCode/distributed_computing*" project and count how any lines contain `if`

6. Create a `diff` file between `findcircles1.py` and `findcircles2.py`.  First make backups of the two files, then: use `patch` to update file 1 to match file 2.  Then use patch again to undo the changes.

7. If you ran the following commands in a folder with one file called `d.txt` what would be the output for each of the following:
```bash
$ ls i_do_not_exist *.txt 2> /dev/null | grep [de]
$ ls i_do_not_exist *.txt 2>&1 | grep [de]
$ ls i_do_not_exist *.txt 2>&1 1>/dev/null | grep [de]
$ ls i_do_not_exist *.txt 1>/dev/null 2>&1 | grep [de]
```

8. Try the `cut`, `join` and `paste` examples from the notes.