# Neoquest Auto - A (Mostly) Automated Neoquest Player

Neoquest Auto is a simple-to-use program built with Python and Selenium that helps users to easily
complete the game and get the game trophies by automating the majority of gameplay including map movement, grinding, 
and weapon upgrades, taking the player all the way from the starting square to the final bosses.
It follows a predefined completion strategy that has been tested and modified over multiple runs 
(not tested on InSaNe mode). 
The only user interaction required is choosing the corresponding program option to complete 
each part of the game.

**2024/04/27 update:** I am not sure when it started, but Neopets has an incredibly annoying sitewide page hiccup that sometimes occurs when performing an action. 
This not only causes page loads to fail in battle, but also causes movement actions to be unpredictably duplicated. 
Unfortunately, this means that **path following/navigation with this program is not reliable right now**, though autobattle/training still handles page load failures properly.

As of now, the program does not keep track of game state on exit.
This may change in the future, but make sure you can run each function to completion before starting.

### Prerequisites

Python 3 or higher - [You can get it from here](https://www.python.org/downloads/)

Google Chrome Browser - [You can get it from here](https://www.google.com/intl/en_ca/chrome/)

Adblock for Chrome - [You can get it from here](https://chrome.google.com/webstore/detail/adblock-%E2%80%94-best-ad-blocker/gighmmpiobklfepjocnamgkkbiglidom)

This program has only been tested for Windows.

### Installing

to prepare the program's starting point, login to Neopets and start a new Neoquest game. Once you see the following
page, you are finished:

![Skillscreen](readmeresources/skillscreen.jpg)

After making a copy of this repository, open the folder in the terminal of your choice and create and activate your
virtual environment (venv). 

[Your virtual environment creation instructions](https://docs.python.org/3/library/venv.html) will differ based on
what terminal you use.

For example, Windows users using Powershell might perform the following commands:

```
py -m venv venv

venv/Scripts/Activate.ps1
```

Once your venv is activated, use the following command to install the necessary requirements to 
your venv:

```
pip install -r requirements.txt
```

The program is almost ready to run. There are two text files in the src/txtfiles folder named userinfo.txt and 
adblockpath.txt. In userinfo.txt, enter your Neopets username on the first line of the file, 
and your password on the second line.

![Userinfoexample](readmeresources/userinfoexample.jpg)

The program can run without adblock enabled, but it will run slowly.
For now, [consult this thread](https://www.reddit.com/r/learnpython/comments/4zzn69/how_do_i_get_adblockplus_to_work_with_selenium/)
for instructions on how to find the path to your adblock extension folder. 
Copy this folder path into adblockpath.txt.
Below is an example of what the folder path could look like for a windows user:

![FolderPath](readmeresources/extensionfolderexample.jpg)

Note: I have tried implementing an "Eager" pageLoadStrategy for the Selenium WebDriver, 
and while it does speed up the program, it is still far slower than blocking ads altogether.

Now, navigate to the src directory and run autoplayerlauncher.py to start the program:

```
cd src

py ./autoplayerlauncher.py
```

The program should now launch and present you the following interface:

![ProgramMenu](readmeresources/programmenuexample.jpg)

At this point, simply make sure you are on the skill screen and enter 1 in the program.
Below is a list of very rough completion times one can expect for each function:

Option 1: 20~ minutes

Option 2: 50~ minutes

Option 3: 3~ hours

Option 4: 3~ hours

Option 5: 1 hour 40~ minutes

Option 6: 55 minutes

Option 7 (end of game): 1 hour 20~ minutes

## Built With

* [Python](https://www.python.org) - The programming language used
* [Selenium](https://www.selenium.dev) - Used for automating browser navigation
