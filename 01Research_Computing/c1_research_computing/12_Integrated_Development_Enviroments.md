# Integrated Development Environments*

The use of Integrated developments like VSCode can make code development much easier and faster.  At the basic level they allow you to write and run you code in a single environment, with built in debugging tools. Modern ones are much more sophisticated than this an perform static analysis of your code to identify errors and formatting issues as you type.  They keep track of the variables you have defined and can autocomplete them for you, this extends to validating that the packages you want to import are installed and highlighting imports that are not used.  They will also provide a GUI interface for git commands and manage connections to remote repositories

This "lecture" is not examinable, and I only provide it so you can see what is possible. I would advise getting to grips with the basics before using to much of the functionality as VSCode automates so much it can stop you learning the material properly (which could become a problem in exams, or if you end up needing to use an environment where you can't use it like on some supercomputers)

There is little point me writing notes with screen shots for this as there are excellent resources online, here are the standard tutorials [here](https://www.youtube.com/playlist?list=PLj6YeMhvp2S5UgiQnBfvD7XgOMKs3O_G6)

To see all you can do just explore the menus or right click in the code window.

## Extensions

VScode's real power comes from its extensions.  Here are some of the ones I use most commonly (for details just click then in the extensions window):
- Language packages (Python, C/C++, Fortran, Julia, CMake) These give language specific syntactical highlighting and helper functions intellisense and snippets specific to each language.  Python allows you to select and manage conda environments and run jupyter notebooks in the editor.
- Spell checking, this is useful for latex or md files.
- Formatters (Black, clang-format) Can be configured to auto-format code on save
- Version control (GitLens ... ) Extended support for managing Git with helper and visualisation tools
- Latex Allow you to develop and build projects in your editor and see the tex and output side by side.  Latex can be configured to build on save
- Docker will allow the building of images by right clicking docker files, images can be run from the side bar.  VSCode provides a link into the container so you can work and edit files as if they were local.
- Remote will read your `.ssh/config` and allow you to connect to remote machines just by clicking.  It will also manage scp so that you can edit and run remote code as if they were local

## Copilot
Copilot is an extension but is a bit more than that in that it will complete coding tasks for you.  It has its own set of tutorials [here](https://www.youtube.com/playlist?list=PLj6YeMhvp2S5_hvBl2SE-7YCHYlLQ0bPt).  It will just suggest code as you type in grey, tab will accept, or you can open a chat window with `cmd+I` and just ask it to do something.  It will be revolutionary for code development, and you should use it as the productivity boost is enormous.  However in this course try not to use it for anything you have not already mastered as then you will not learn it.  
