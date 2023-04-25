![img1](https://raw.githubusercontent.com/mimseyedi/gerdoo/master/docs/imgs/gerdoo_poster.png)

 ## Table of Contents: <a class="anchor" id="contents"></a>
* [What exactly is gerdoo?](#gerdoo)
* [How to install](#install)
  * [gerdoo Installer](#gerdoo_installer)
  * [Clone the repository](#clone)
* [How does gerdoo work?](#work)
  * [Launcher](#launcher)
    * [gerdoo Updater](#gerdoo_updater)
  * [Shell](#shell)
  * [Kernel](#kernel)
    * [How kernel runs porgrams?](#kernel_runs)
    * [PIF](#pif)
  * [Programs](#programs)
    * [Built-in programs](#bins)
    * [Standard Programs](#stnd)
    * [External Programs](#extn)
  * [Modules](#modules)
    * [gerdoolib](#gerdoolib)
* [Contribute](#contribute)
  * [The structure of program development](#structure)
  * [Development of gerdoolib](#gerdoo_lib_dev)
  * [Using the issues section for ideation](#idea)
  * [Development of gerdoo with other languages](#lang_dev)
* [Resources](#resources)


## What exactly is gerdoo? <a class="anchor" id="gerdoo"></a>
gerdoo is a personal `CLI` assistant.
With gerdoo and with the help of smaller programs or `Python` scripts (and in the future with other languages), you can run your programs in an environment similar to the terminal space and create a comprehensive program for doing your daily tasks and `personal commands`. A high-speed and fully customized program, it runs the programs you wrote yourself in an integrated environment, and it is even provided as `open source` in the form of a `GPL license`, so that you can apply any changes you want.



## How to install <a class="anchor" id="install"></a>
There are `two` main ways to install gerdoo.


You can download the complete repository with `git clone` or use the `gerdoo installer`. There are instructions for both methods here, but I `suggest` you use the `gerdoo installer` itself.

**Required: You need Python version 3.11 or higher to run gerdoo.**

## gerdoo Installer <a class="anchor" id="gerdoo_installer"></a>

Using `curl` to download gerdoo installer:
```
curl -o gerdoo_installer.py https://raw.githubusercontent.com/mimseyedi/gerdoo/master/inst/gerdoo_installer.py
```

Then running `gerdoo_installer.py`:
```
python3 gerdoo_installer.py
```

After the installation, go to the `installation location` and run the `gerdoo.py` file:
```
python3 gerdoo.py
```

## Clone the repository <a class="anchor" id="clone"></a>

Using `git clone` to download gerdoo repository:
```
git clone https://github.com/mimseyedi/gerdoo.git
```

Then you need to change some `settings` for gerdoo to run properly. (There is no need to do this in the gerdoo installation method by the gerdoo installer, and these changes are applied in the installation process)

Go to the `setg` directory and open the `PATH.json` file in a simple editor and then enter the path of the directory you want as the `home directory` in front of the `home` key.

**The home directory means the directory that when gerdoo starts working, it places your directory in its path.**

**PATH.json**
```json
{
  "home": "/a/b/c"
}
```

Then, in the same directory `(setg)`, open the `PASS.json` file in the editor and enter the password `hashed` with the `sha256` algorithm in front of the `user_pass` key.

**Note: the password must be hashed by sha256 algorithm.**

You can use this link https://emn178.github.io/online-tools/sha256.html to hash your password first, and in the next steps, you can use the `setg program` inside gerdoo to `change` the password.

**PASS.json**
```json
{
  "user_pass": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
}
```

After performing these steps, now it's time to run the main program `(gerdoo.py)` in the `directory or the main path` of the program:
```
python3 gerdoo.py
```

## How does gerdoo work? <a class="anchor" id="work"></a>
![img2](https://raw.githubusercontent.com/mimseyedi/gerdoo/master/docs/imgs/how_the_gerdoo_works.png)

When you run the `gerdoo.py` program with the Python interpreter, at first, if you are connected to the Internet, the `gerdoo_updater` program will run, and the task of this program is to check and install the `available updates`. Then the first program that runs is the `shell`, which is the `main interface` of gerdoo. The shell is the communication between the `user` and the `kernel`. Kernel is a program that interprets `user commands` and `executes` and manages `programs`. The programs are divided into `three` categories: `built-in` programs, `standard` programs, and `external` programs, which I will introduce further.

## Launcher <a class="anchor" id="launcher"></a>
The main gerdoo launcher is a `Python` file in the `main path` of the program called `gerdoo.py`.
The task of this program is to check the `Python version` to allow access to the program and to run the `gerdoo_updater` program and finally the `shell`.

## gerdoo Updater <a class="anchor" id="gerdoo_updater"></a>
The task of the `gerdoo_updater` program is to check `updates` for the `main gerdoo programs` such as `kernel`, `shell` and the main gerdoo module, `gerdoolib`. This program receives update information by connecting to the `GitHub repository` and then performs the `installation` process.

## Shell <a class="anchor" id="shell"></a>
The `shell` program is the `main interface` of gerdoo and a `bridge` between the `user` and the main gerdoo `kernel`. Commands are sent to the `kernel` through the `shell` and the answers are `returned` to the `shell`. The `shell` program uses `completer menus` to provide `easier access` for the user to the `contents` of the `directories`. Also, the `shell` saves the user's `previous` commands in its `short-term memory` so that the user can easily `switch` between their `previous commands` with the `up` and `down` keys.

## Kernel <a class="anchor" id="kernel"></a>
The task of the `kernel` program is to `interpret` the `user commands` that came from the `shell` and `execute` the programs and manage the `response` to the user.

`Kernel` searches the programs according to the user's request and executes the program `related` to the user's command and passes the `arguments` entered by the user to the program.

## How kernel runs programs <a class="anchor" id="kernel_runs"></a>
`Kernel` executes the programs by seeing the file containing their `information` **(PIF)**.
The execution information of the program is `stored` in these files, and the `kernel` executes the execution `instructions` of each program by `reading` this information.
## PIF <a class="anchor" id="pif"></a>
`PIF` (Program Information File) is a file in `json` format that holds the `necessary` information of each `program`. Every program has a `PIF` file with the `same name` as the program, which kernel reads the `required` information and `executes` the program according to that information.

<br>

KEY|TYPE|DESCRIPTION
---|----|---
name|string|Program name
version|string|Program version
author|string|Program author
description|string|Program description
executable|string|The path or file name that the kernel should execute
plugins|list[str]|Files that must exist in the path of the program so that the program runs correctly.
requirements|list[str]|Python packages that the program needs to run.

<br/>

**An example of a program's PIF:***
```json
{
  "name": "this",
  "version": "1.0.0",
  "author": "mimseyedi",
  "description": "This program displays the main information of gerdoo.",
  "executable": "this.py",
  "plugins": [],
  "requirements": ["click"]
}
```

## Programs <a class="anchor" id="programs"></a>
Programs are `Python files` stored in directories with `program names`. Each program consists of a `Python file` and a `json` file known as `PIF` (Program Information File), which stores `information` about the program.

## Built-in programs <a class="anchor" id="bins"></a>
`Built-in` programs are the programs that are `closest` to the kernel. These programs are stored separately in a directory called `bins`, in the `kernel directory`, but they are `called and executed directly` from within the `kernel`.

The reason for calling and running these programs directly inside the kernel is `limited access` that cannot be had from the `outside`. For example, changing the `work directory` cannot be done from an `independent` program and must be done in the `kernel`.

However, for easier development, each of the `built-in` programs can be operated independently like other programs, and only a `function` named the same program is `called` in the kernel to be a `bridge` between the `kernel` and the `executable file` of the program.

## Standard Programs <a class="anchor" id="stnd"></a>
`Standard` programs are among the programs that are `installed` along with `gerdoo`. These programs were `written` and `developed` by me and are `examples` of `standard gerdoo programs`. These programs are not as `basic` as the `built-in` programs, but their presence can be very `helpful`. For example, you can `download` and `install` other programs from the `repository` with the help of a `standard` program called `install`. Or you can `delete` a `directory` using the `deldir` program and...

These programs are `stored` in the `programs folder` called `prgs` and in the `stnd` directory.

## External Programs <a class="anchor" id="extn"></a>
`External` programs are programs that the user can `choose` to install. These programs can have `various` functions and they will `not` be `installed` together with `gerdoo` when `installing` gerdoo, and they must be `downloaded` and `installed` separately, which can be easily done with the help of a `standard` program called `repo`. With the help of this program, you can find out about the `status` of other programs and view their `descriptions` and `versions`, and then `install` or `update` the programs with the help of the `standard` `install` and `update` programs.

## Modules <a class="anchor" id="modules"></a>
Modules can exist to make things `easier` for `developers`. The first module written by me is `gerdoolib`, whose functions can be used to make it easier to develop programs or even `gerdoo` itself.

## gerdoolib <a class="anchor" id="gerdoolib"></a>
`gerdoolib` is currently a very simple `module` that can help `program developers` to a good extent. For example, `gerdoolib` can help developers to `print messages` in various modes under gerdoo `standards`. Or, for example, there are functions that can help developers to `authenticate`, `get versions` and `descriptions` of programs, read `PIF` information, etc.

## Contribute <a class="anchor" id="contribute"></a>
`Contribution` in the development of `gerdoo` is the most `important` part of this project. I think that gerdoo can be a very `flexible` program. The `philosophy` and `nature` of gerdoo is very `simple`, but it can use `complex` and `diverse` programs to become `bigger` and more `practical`. Also, if needed, it can be a `very personal` program for users to `execute` their `personal commands` with it and enjoy. I `suggest` that even if you use gerdoo as a completely personal program, you `share` your programs so that others can `use` them and maybe `develop` them.

## The structure of program development <a class="anchor" id="structure"></a>
All programs in gerdoo have a `common structure`. Each program has a `specific directory` that contains the program's `executable file` (a Python file), a `PIF` file in json format, and, if `necessary`, `side files` related to the executable file.

All programs written in gerdoo use the `click` module. This module is a `CLT` (Command Line Tools) and allows you to develop your programs faster under the terminal. It is `suggested` to use this module to develop your programs, which you can get guidance from <a href="https://click.palletsprojects.com/en/8.1.x/">here</a>. But there is no insistence to work with this module and write your programs as you are `comfortable`.

If you like, you can write and develop `external` programs to increase the efficiency of gerdoo or strengthen the infrastructure of gerdoo and strengthen the main pillars by developing `standard` programs and `main gerdoo programs`.
## Development of gerdoolib <a class="anchor" id="gerdoo_lib_dev"></a>
You can also develop the main gerdoo module called `gerdoolib` and make the work of developing programs `easier` for other developers.
You can also write your own `modules` and add them to gerdoo so that others can `use` them.

You can also `translate` the modules into `other languages` to create a suitable infrastructure for the development of gerdoo with other languages in the `future`.

## Using the issues section for ideation <a class="anchor" id="idea"></a>
The `issues section` can be used both for `reporting problems` and for `generating ideas` so that others can get to know your ideas and maybe this is a `good motivation` for them to `start working`.
So, go to the `top menu` of the `repository page` and check the `issues` section!

## Development of gerdoo with other languages <a class="anchor" id="lang_dev"></a>
An interesting idea for gerdoo development is to develop gerdoo with `different programming languages`. In the `test version` of gerdoo, I was able to make the kernel `compatible` with `C++` programs, and I developed part of the `standard` programs with `C++`. But I had a problem compiling and running `C++ programs` in the `Windows operating system`, which I `ignored` for now, but I am going to `work on it`. (In `Unix` operating systems such as `Linux` and `MacOS`, you can easily `compile` and run `C++` codes with the built-in `g++` compiler).

If you want to develop gerdoo in a language you like, go ahead and look at the `kernel code` and find a way to do it.

## Resources <a class="anchor" id="resources"></a>
I used the following resources and modules to develop gerdoo:

* [click module](https://github.com/pallets/click/)
* [requests module](https://github.com/psf/requests)
* [prompt_toolkit module](https://github.com/prompt-toolkit/python-prompt-toolkit)
* [clint module](https://github.com/kennethreitz-archive/clint)
* [Canva](https://www.canva.com/)