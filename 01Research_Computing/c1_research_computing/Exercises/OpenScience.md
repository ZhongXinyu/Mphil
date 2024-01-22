# Open Science Examples
Only one problem this week which is put everything together into one helper script!

## 1. Setup
Create a `bash` script which takes a project name as input and generates a blank repo with the standard materials needed for good practice.

If you can, see if you can do the following:
- Create a directory with the project name
- Enter the directory and create the following sub directories:
    - src
    - test
    - docs
    - ?? (what else would you like?)
- create a `.gitignore` file
- create a `.pre-commit-config.yml`
- create a `Doxyfile` and configure it for the repo (to replace lines use: sed -i '.bak' 's/**oldline**/**newline**/' /path/to/file)
- initialise git
- ask if you want to use an existing conda environment or create a new `conda` environment with the project name and standard packages.  If so create the environment and install the standard packages: 
    - pre-commit
    - pytest
    - black
    - flake8
    - configparser
    - numpy
    - pandas
    - scipy
    - matplotlib
    - ?? (what else would you like?)
- Install pre-commit
- Create a README.md with the project name and basic structure
- Export the current conda environment to environment.yml
- Build a basic dockerfile
- create first commit
- use GitHub/GitLab/etc.. API to create/connect to a remote repo and push this first commit to it
- display success message!

Some of this is tricky so make sure you test it in a safe environment (i.e. not near any work you like!) and test small sections at a time. Bonus points for error traps that stop this all going horribly wrong! If you do a good job you are partway done with all your course work for the rest of the year!  Don't worry if it's too hard, we didn't do much on scripting, and I will give out a solution.  You can do most of this in python too if you want which will make some bits easier (and some bits harder).

