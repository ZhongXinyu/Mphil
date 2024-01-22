# Open Science

Increasingly there is a requirement to not only publish your work in a paper but to also make your data and code available so people can reproduce your results.  Now the requirement for code to be public is often baked into the public funding of experiments.  

This can sound scary at first as sharing your code feels like giving away your work while exposing yourself to criticism if people find bugs.  One of the key goals of this course is to provide you with the skills to ensure that you write code that you can be proud of, and which has validation builtin.  Also making code public can be one of the best ways of attracting people to your work.  By making your pipelines available to others ensures a large number of citations from everyone who uses them and ownership of public codes has been the cornerstone of many an academic career.

This lecture discusses how best to go about this.

## Sharing Code
Sharing your code is easy if you host it on a git server you can link to it in your papers and anyone can clone and use it.  People can even make improvements create pull requests for you to review and include if you want.  You also have the option to submit your code for review, just like you do for papers, to places like the Journal of Open Source Software where you will get expert input into how to improve your code.

You should always include:
-   Licence, just use a standard open source licence (see here: https://opensource.org/licenses).  You can use this page to select which one is most appropriate: https://choosealicense.com
- README.md, a file which tells the user about the project.  It should include the following information:
    - Title
    - Description + motivation
    - Contents (optional)
    - Installation
    - How to run/use the project
    - Features
    - Frameworks (Languages/Testing/CI/Containerisation)
    - Build status / Known bugs / version info (optional)
    - Credits

## Sharing Data
In order for people to use your code they will need to have access to any data sets required for the project.  Do not include these in the github unless very small (and preferably text).  Data sets should be available via public servers and it is helpful to provide `bash` scripts that download the data for them.  The key command for this is `curl` or `wget`.  `curl` is great for files and supports a much larger range of transfer methods. It can transfer in parallel, can automatically compress data using `--compressed`, and is available at standard on most platforms. `wget` is narrower but does have the ability to pull whole directories using the option `--recursive` (you can avoid this by packaging the files together with `tar` before transfer with `curl`) and can recover from broken connections if the internet is unreliable which `curl` cannot.  `wget` can sometimes do compression with the flag `--compression` but it depends on how it was built (as it uses a different library to do this, it is not intrinsic to the command)

```bash
$ curl https://weblink_to_the_data.zip --output local_file_name.zip
$ unzip local_file_name.zip
```
or
```bash
$ curl https://weblink_to_the_data.zip | jar xv
```
if you have `jar` (which is java not bash but often included)

## Sharing Enviroment
In order to fully replicate your results you also need to be able to share the language and package version that you used to run the code.  There can be subtle differences between package and language versions which can change the results or cause the code to crash so it is important to include this information in your repositories.

For Python this can be done using either the pip or conda environment files.  Remember to create them in a **build independent** way otherwise the environments will not be able to be created on different operating systems.

```bash
conda env export -n enviroment_name -f environment.yml --no-builds
```

You should update this whenever you push to `main` in your git repo.

This is still not perfect as some packages may not be available on every operating system.  What we want is to be able to share the entire computing space that we use.  This is where virtualisation comes in.

We have been using virtualisation already via `conda` which created virtual environments.  This creates an virtual environment to house python, its packages, and dependencies.  These are light-weight and easy to manage, (it basically just updates you `PATH` to point to different folders), but, as all virtual environments share the same OS and most environment variables, they are still able to interact significantly and are OS specific.  

To completely avoid this we need to create virtual machines.   Virtual machines virtualise the computer hardware itself (access to the actual hardware is now managed by a hypervisor rather than the OS kernel).  This allows each virtual machine to have its own Kernel, OS, software, everything.  These are quite heavy duty as each image contains duplicates of all the software required so are often very large in memory.

There exists a middle ground between the two options, containers.  Here we virtualise the OS (which leverages some of the existing OS, so can be very small, as little as 5Mb).  This allows for most of the advantages of virtual machines without the heavy memory load.

## Containers
Containers have become very popular since the creation of Docker in 2013 and is being driven by the rise in cloud computing.  The issue was that if companies switched cloud provider then their systems would stop working due to environment or chip changes which can be a pain to resolve.  Docker solves this by creating small virtual OS which are identical on any machine.  This makes applications much more stable and portable, applications can also be run on machines without installing any packages, or even the language interpreters.  This is exactly what we are looking for when we share our code but can also be useful for when we switch between different computing resources ourselves, say department linux desktops and mac or windows laptops.  A well written Docker project can move seamlessly between everything with minimal effort.  Often cloud providers require dockerfiles in order to connect to Git repositories so if you want to use these resources you will need to learn how to create them.

### Getting started
First we need to install Docker.   To do this just navigate to the Docker webpage and click download.  You will need to start the application whenever you want to use it.  To check it is running, try the following in a terminal:
```bash
$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
Now Docker comes with some jargon which we have to get used to:
- Container
- Image
- Dockerfile

In reverse order, a `Dockerfile` is a list of instructions for building an `image`.  An image is file, which describes the exact software setup required for the environment.  It is stored in layers from OS up to applications.  This allows images to build on each other so a `python image` can be build from an `ubuntu image`. Each layer can be cached to improve subsequent loading performance.  A `container` is the computing environment created when we are running an `image`.  It is where we can run the code we want to.

We don't have to start from scratch when creating containers as Docker has `docker hub` which has a large library of images you can use.  It is to images, what GitHub is to code.  In fact Docker is often called the "git of containers"

If we go to: `https://hub.docker.com` we can search for any images we want to use.  These are just `Dockerfile`s which contain instructions for building images

You need to `pull` image from dockerhub from the command line using:
```bash
$ docker pull continuumio/miniconda3
or
$ docker pull python
```
You can see the images you have pulled with:
```bash
$ docker image ls
```
To create a container from the image we just need to run it:
```bash
$ docker run continuumio/miniconda3
```
which runs then immediately exits.  To have the environment persist, and for us to be able to interact with is we need to add the following options -d (detached) -t (allocate a pseudo-TTY or terminal).  We can also add a name for the container using the option `--name`
```bash
$ docker run -d -t --name=conda continuumio/miniconda3
```
If we look at our running containers we can see it:
```bash
$ docker ps
```
Now that it is running in the background.  How do we access it?  We can ask the container to run a bash terminal for us using the `exec` command:
```bash
$ docker exec -ti conda bash
```
Now we can access a linux machine with miniconda installed (try `$ conda` to see it).  You can then install packages using conda in this container the way you normally would.  There is no need to create a virtual environment (unless you want to have two or more) as the container has already separated your environment from your system. You can see this by doing an `ls` which will only show the standard folders for a minimal linux machine.

To stop containers we just need to type:
```bash
$ docker stop conda
```
and if we check running containers we can see it had gone:
```bash
$ docker ps
```
However the container persists is a stopped state which blocks us from creating it again with the same name (this is for caching reasons, it will stop eventually). You can see this with
```bash
$ docker ps -a
```
We can remove it properly with
```bash
$ docker rm conda
```
And now we can create it again:
```bash
$ docker run -d -t --name=conda continuumio/miniconda3
```
We can avoid this complication by using --rm:
```bash
$ docker run --rm -d -t --name=conda continuumio/miniconda3
```
which removes the container on a stop.

If we look at the container we find that the packages we installed last time are now gone! This is because we never added them back to the `image` we used to create it.  In order to keep changes we need to `commit` our changes (just like `git`)
```bash
$ docker commit 'container' 'image'
```
which creates a new image from the container
```bash
$ docker image ls
```

Putting your code into a container brings some extra challenges as now the container running your code is independent from you local machine and you cannot pass files or data between them.  We will quickly look at two issues and how to resolve them

### Connecting Jupyter to your Browser
When you run Jupyter notebooks or Jupyter lab they normally open automatically in your browser.  You can try to launch them on you container using the following
```
jupyter lab/notebook --ip='0.0.0.0' --port=8888 --no-browser --allow-root
```
but this does not work as the container and local system can't talk to each other, and the container has no browser to host it.  In order to view the output we need to open a connection between the container and our local machine.

To do this we need to stop the container and restart it with:
```bash
$ docker run --rm -d -t --name=conda -p 8888:8888 continuumio/miniconda3
```
which maps between: local machine port -> 8888:8888 <- container port
```bash
$ docker exec -ti conda bash
$ jupyter lab/notebook --ip='0.0.0.0' --port=8888 --no-browser --allow-root
```
Now if we go to our browser and navigate to `localhost:8888` (and input token) we can access the notebook and run code. 

### Mapping local folders into containers
The other issue we have is that we may want to be able to access data on our local machine from our container.  To do this we have to mount local folders as volumes on the container.  This is done via the command
```bash
$ docker run --rm -d -t --name=conda --mount src=/local/folder, target=/container/folder,type=bind continuumio/miniconda3
```
Which creates a folder in the container called `/container/folder` which had mounted the host folder `/local/folder`.


## Automating Images
While we can create images interactively like above, we would like to be able to create the containers automatically for when we move machines or for sharing the project with other people. In order to do this we have to create a `Dockerfile`, which is a set of instructions for building a docker image.

If we go to Docker Hub we can see that this is all we are doing when we pull and image from here. `Dockerfile`s can reference other `Dockerfile`s so you can build up complex environments easily.

You don't want to have to start from scratch (as there are already excellent Dockerfiles for clean operating systems you can use which will be smaller than any you would create).  You can import any image from Docker Hub using the command `FROM` which works just like `docker pull` from earlier.  To create the basic image for miniconda that we did earlier we just need to create a Dockerfile which contains a single line:

```Dockerfile 
FROM continuumio/miniconda3
```

then to run you type:
```bash
$ docker build -t conda .
```
where `-t conda` attaches a **t**ag and `.` says look in the current folder for the `Dockerfile`.  It should always be called `Dockerfile`

This creates the image and
```bash
$ docker run --rm -ti conda
```

Uses the image to create the container.  To connect a local folder to the image

```Dockerfile 
FROM continuumio/miniconda3

COPY /source/folder /destination/folder

WORKDIR /work/directory
```
You also have the command ADD which works the same as copy but also expands `.tar` files. In general COPY is preferred for everything else.

It is important to note that `docker` also works for `urls`.  You can build git repositories using

```bash
$ docker build github.com/fruzsinaagocs/oscode
```

It is important to note that almost every command in the `Dockerfile` creates a `layer` in the resulting image.  Each layer is cached so when you build a second time they will pop up immediately.  If a layer changes then all subsequent layers are rerun so you have to be careful about the order that you list commands.

You can run commands using the `RUN` command, for example installing software:
```Dockerfile
FROM ubuntu

RUN apt-get update && apt-get install -y \
    python3 \
    python-pip

COPY /source/folder /destination/folder
WORKDIR /work/directory
```
but `RUN` will do any command the terminal would (it is strongly recommended that you always `RUN apt-get update && apt-get install` commands in one line for caching reasons).  Note that as order is important (as if a previous layer changes all subsequent layers will run).  If the `RUN` and `COPY` were reversed then each time a file changed in the mounted directory we would try to reinstall python.


If you use conda you can do:
```Dockerfile
FROM continuumio/miniconda3

RUN mkdir -p project \
    && git clone https://github.com/remote-repo/project project/

RUN cd project \
    conda env update --file environment.yml --name base

RUN mkdir -p data \
    && curl -SL https://datastore.com/data.tar.xz \
    | tar -xJC /data
```

Note: some linux versions will not have `git` installed so you will need to do this manually,
```Dockerfile
RUN apt-get update && apt-get install -y \
    git
```

Finally if you want to be able to use jupyter notebooks or jupyter lab then you will need to specify the ports the same as above when creating the image and running the command in the container.  It is also good practice to explicitly expose the port in the Dockerfile using:
```Dockerfile
EXPOSE 8888
```

There is much more you can do with docker which I will leave you to find when you need it via google. I will just add the note that it is great to add Dockerfiles to repositories which you make public as they significantly increase there usability.