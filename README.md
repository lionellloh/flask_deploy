# smartbin-server
server end of the smart bin

## What's in here?
- Server app
  - for generating the leaderboard
  - handling requests from the Pi (client)
- Web page templates
  - tell the server how to convert database info into pretty web pages
- Database code (SQL)
  - for storing user info and stats

## How do I use GitHub??
First create a GitHub account and apply for access to the code (we'll call this collection of code a "repository" or "repo" for short).

Then clone the repository to your computer. In PyCharm, from the default screen, select "check out from version control". The simplest way to connect PyCharm to your GitHub account is to select the GitHub option and enter your username and password.[^1]

Make edits as normal. Then when ready to upload your code, click on "VCS" > "Commit Changes...", select the files you want to upload, enter a descriptive message about the changes you made, then select "Commit" > "Commit and Push".

Advanced Git features like branch, revert, merge, stash, diff, etc are. worth the time and effort to learn if you are thinking about ISTD/CSD/whatever it's called nowadays, or simply going to work on other, bigger code projects in the future.

## Technical details
For now, I am using:[^2]
- Python 3.6.1
- Flask (simple web server framework)
- Gunicorn (simple HTTP server that can handle multiple requests at once)

Data layer is probably going to be SQLite or similar lightweight relational DB system.

For development and testing it is probably sufficient to run the server on your own computer and point the client to your computer (you may need to be on the same wifi network to do this).

Deployment can be done on [Heroku](https://www.heroku.com/) (which does not support SQLite but supports PostgreSQL, which is much more powerful beast) or alternatively on my own lepak.sg server which does have a [Heroku-like deployment interface](http://dokku.viewdocs.io/dokku/).

### Virtual environment

It is highly recommended to set up a "virtual environment" (virtualenv), which basically lets multiple Pythons live together on the same computer, each with its own set of packages of different versions. You may already have seen some of the chaos that can happen when you let too many Pythons loose in your computer, if you used Mayavi in your DW/Chem 2D.

- If you are using PyCharm, you can do this relatively easily. Refer to the [PyCharm manual](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html) for instructions. PyCharm should prompt you to install packages when you open `requirements.txt`.
- If you are using Spyder, you will need to add a new conda environment either through the Anaconda Navigator interface or using `conda env`.
- All others (VS Code, Sublime, Atom, Notepad etc): either refer to your IDE's specific documentation or else create your own virtualenv like this:

      $ cd /to/the/project/root/
      $ virtualenv -p python3.6 .
      $ pip install -r requirements.txt

  In this configuration, make sure you do not commit virtualenv directories into GitHub! I have set up `.gitignore` to do this already, but just make sure.

## What needs to be done?

- Decide the API to implement
- Server code
- Database code
- Template code
- HTML, JS etc etc
  - You can use any framework you want to create your pages; Flask and Jinja2 do not know anything about web page frameworks, they only run the commands in curly braces.

---

[^1]: The recommended way is to generate a new GitHub token for PyCharm but this is a little more complicated.

[^2]: This configuration is technically able to be deployed as-is but it is recommended to run Gunicorn behind a proxy server like nginx.