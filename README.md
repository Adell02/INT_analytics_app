<div id="top"></div>

<h1 align="center"> INT - RAY PROJECT (Data Analysis Web App) </h1>

<p align="center">Web app enclosing INT technical project. This repository includes the necessary files and instructions to run the app. The aquitecture is based on a Flask app (running a Python backend and html/css/js based frontend)<br>[The production branch is running on an AWS server @ 51.20.95.113]</p>
<br />

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#Install">Install</a></li>
    <li><a href='#Git Frequently Used Commands'>Git Frequently Used Commands</a></li>
    <li><a href="#File Structure">File Structure</a></li>
    <li><a href="#User Experience">User Experience</a></li>
    <li><a href="Backend Breakthrough">Backend Breakthrough</a></li>
        <ul>
            <li><a href="#Private MySQL Database">Private MySQL Database</a></li>
            <li><a href="#Authenticaiton and Security">Authenticaiton and Security</a></li>
            <li><a href="#Graphs Computation">Graphs Computation</a></li>
        </ul>
    <li><a href="#roadmap">Roadmap</a></li>

  </ol>
</details>


<!-- Install -->
<div id="Install"></div>

## Install

Install **VSCode** and **Python 3.11.5** in your machine.

Open VSCode and select **Clone Git Repository** option from the main screen.

Copy and paste the following URL:
```sh
https://github.com/Adell02/INT_analytics_app.git
```

Login to GitHub, if necessary

> **_If running in Windows OS:_** 
> 
> Click "Terminal" (at the top bar in VSCode) and select a **New Terminal**. 
> 
> In the upper-right part of the terminal console, click the arrow facing downwards, at the right of a plus (+) sign. 
> 
> Select **Git Bash** From the menu.


Create and activate the virtual environment:
```sh
MAC OS
--------------------------
$ python3 -m venv ./venv
$ source venv/bin/activate

WINDOWS OS
--------------------------
$ python3 -m venv ./venv
$ source venv/Scripts/activate
```
VSCode selects the available virtual environment in the project by default. To check it, just open any ".py" file and look at the bottom of the screen you should see "Python 3.11.5 ('venv':venv)


Install all required libraries in the virtual environment:
```sh
$ pip install -r requirements.txt
```

Now, you can start coding!

<p align="right">(<a href="#top">back to top</a>)</p>

## Git Frequently Used Commands
<div id="Git Frequently Used Commands"></div>

[Most of the content in this section has been extracted from the manual page "man"]

**git add <file_name>**
Files can be added to the index. This is equivalent to VSCode's "Staged Changes". 

**git stash**
Stash the changes in a dirty working directory away. This is, if you want to keep your local changes, but push some of them to git, stash the ones which souldn't be uploaded.
Stashed changes can be later recovered or deleted.

**git pull --rebase**
Fetch from and integrate with another repository or a local branch. Your local repository should be commited or stashed before pulling. "--rebase" option rebase the current branch on top of the upstream branch after fetching.

**git commit -m "<Comment_Description>"**
Record changes to the repository. Create a new commit containing the current contents of the index and the given log message describing the changes. This usually comes right before a push. It should be though of code versions "nodes" linked together: 
<p align='center'>
--( C1 )---------( C2 )---------( C3 )
</p>

**git push**
Update remote refs along with associated objects. This is uploading the commited changes. 


## File Structure
<div id="File Structure"></div>

A breakdown of the file structure is shown next.

<details>
  <summary>Show Structure Tree</summary>

>
\\__ app<br>
..... \\__ database<br>
........... \\__ dfs<br>
........... \\__ cache<br>
........... \\__ models.py<br>
........... \\__ seeder.py<br>
..... \\__ routes<br>
........... \\__ ai_chat.py<br>
........... \\__ analytics.py<br>
........... \\__ auth.py<br>
........... \\__ dash.py<br>
........... \\__ mapview.py<br>
........... \\__ newgraphic.py<br>
........... \\__ production.py<br>
........... \\__ RESTful_API.py<br>
........... \\__ settings.py<br>
..... \\__ static<br>
........... \\__ css<br>
................. \\__ ai_chat.css<br>
................. \\__ analytics.css<br>
................. \\__ auth.css<br>
................. \\__ dashboard.css<br>
................. \\__ main.css<br>
................. \\__ mapview.css<br>
................. \\__ newgraphic.css<br>
................. \\__ production.css<br>
................. \\__ settings.css<br>
........... \\__ js<br>
................. \\__ chat_ai.js<br>
................. \\__ load_graphs.js<br>
................. \\__ map.js<br>
................. \\__ searchable_dropdown.js<br>
........... \\__ gif<br>
................. \\__ R.gif<br>
................. \\__ eds_icon.ico<br>
................. \\__ eds_icon_transparent.png<br>
..... \\__ templates<br>
........... \\__ ai_chat.html<br>
........... \\__ analytics.html<br>
........... \\__ change_password.html<br>
........... \\__ confirm_email.html<br>
........... \\__ dashboard.html<br>
........... \\__ login.html<br>
........... \\__ mapview.html<br>
........... \\__ newgraphic.html<br>
........... \\__ production.html<br>
........... \\__ register.html<br>
........... \\__ settings.py<br>
........... \\__ template.html<br>
..... \\__ utils<br>
........... \\__ account<br>
................. \\__ token.py<br>
........... \\__ AI<br>
................. \\__ openai_request.py<br>
........... \\__ communication<br>
................. \\__ mailing.py<br>
........... \\__ DataframeManager<br>
................. \\__ DataBase.py<br>
................. \\__ dataframe_storage.py<br>
................. \\__ dataframe_treatment.py<br>
................. \\__ from_server_to_df.py<br>
................. \\__ load_df.py<br>
................. \\__ param_battery.json<br>
........... \\__ graph_functions<br>
................. \\__ analytic_functions.py<br>
................. \\__ consumption_vs_temp.py<br>
................. \\__ generate_analytics_graphics.py<br>
................. \\__ generate_dashboard_graphics.py<br>
................. \\__ generate_map.py<br>
................. \\__ parse_json_functions.py<br>
................. \\__ plots_generation.py<br>
................. \\__ dashboard_config.json<br>
................. \\__ analytics_config.json<br>
..... \\__ __init__.py<br>
..... \\__ config.py<br>
\\__ README.md<br>
\\__ .gitignore<br>
\\__ requirements.txt<br>
\\__ run.py<br>

</details>
 
 A description of every directory up to a second-level depth is described below.

 - **app**: contains every file conforming the app itself (frontend/backend).
 - **database**: contains files regarding data caching, user models (classes), MySQL and SQL related functions. 
 - **routes**: contains every python file organized in "Blueprints" (functionalities) for the backend.
 - **static**: files such as css,js and gifs are stored in this directory. JS files include loading (and optimizing) graphs in their containers and displaying messages in the AI Chat.
 - **templates**: contains the respective html template for every Blueprint (declared in routes). Additionally, there is a main template on which every page extents that displays the sidebar and loads some js/css resources common in all pages.
 - **utils**: backend auxiliary functions are stored in this directory. Its sublevel has the following directories: account (token generation and validation), AI (OpenAI requests functions), communication (sending email features), DataframeManager (parsing raw strings and dataframe/.parquet generation functions), and graph_functions (graph computation functions).

 **__ init__.py** : It contains the main "create_app" function that initializes the app. In it, every main object such as Flask or Session are instantiated. Blueprints are imported and included in this file. 

 **config.py**: main app configurations are set in this file. Environment variables are also loaded in this file.

 **run.py**: Main file containing the execution of "create_app" function in __ init__.py module.


## Backend Breakthrough
<div id="Backend Breakthrough"></div>

Although the code itself it's meant to be commented and self-explanatory, the following subsections describe meticously each main functionality implemented in the backend code.

#### Private MySQL Database
<div id="Private MySQL Database"></div>

Electronic Data Services has deployed a MySQL server in the Ubuntu AWS machine used for production deployment. Although other configurations are preferred, it's a valid implmentation for a prototype product. In it, information about users and their data is stored. To access it, a MySQL cursor is used. All functions to add/remove/fetch/edit any field in it is available in "seeder.py". It is worth mentioning that these functions are wrapped with a wrapper that manages the opening and closure of connections. 

#### Authenticaiton and Security
<div id="Authenticaiton and Security"></div>

Users information such as email, password, role, tokens, organization name and confirmation are stored in our private database. Different fields are stored in different manners, the next bullet points describe how it is done for every parameter:
- email: Directly stored when registered. Can't be modified.
- password: Stored when registered, hashed with a secret key. Can be changed with the function "change_password" in "auth.py", accessible through _/change_password/\<token>_ or using the link attached in the settings page for every user (when logged in).
- role: Automatically assigned to 'user'. Not functional by the moment.
- tokens: Every user owns a unique token that can be shared with others and it's automatically generated when signs up (available in settings page, when logged in). On the settings page, users can paste a token from another user to build up a shared dashboard. This one is originally set to a _Null_ value.  
- confirmation: Automatically set to False. Can be changed by an admin, as seen in <a href="#user-experience"> User Experience.Authentication</a>

#### Graphs Computation
<div id="Graphs Computation"></div>

In "dash.py", the code ran to compute 



## User Experience
<div id="User Experience"></div>

This app mainly runs on hmtl/js/css frontend with a main Python backend framework.

The app's operation principle regarding a regular user is described next.

**Authentication**: "auth" blueprint contains every authentication-related functionality, such as registering, logging in, or wrappers to check whether the user is logged in or not. 

To keep it safe, registering is publicly allowed, but confirmation is required to definetly accept a log in. To do so, an administrator/developer can make use of the func tions located in "seeder.py". 

>_By the moment (19th Nov. 2023), this function is reachable from the developing branch of the project, calling the url localhost/confirm_user. Thus a prompt will show up in the terminal, where the email address of the user to validate should be introduced. Finally, a message will appear on the screen indicating that the user has been confirmed._

The developer can see users' available information by accessing _localhost/fetch_all_ or _localhost/fetch_user/\<email>_, when running the app locally. 

**Accessing The App**: Once the user is registered, confirmed and logged in the app, they will be automatically redirected to their dashboard ( _/private/dashboard_ ). 

**Moving Through Pages**: Using the left-side bar, the user will be able to change page within: Dashboard, Analytics, New Graph, Mapview, and AI Chat.

**Important Note**: It is important to log out when users are done with their activity. It is a relevant security method to avoid retaining critical information in their browser session.


<!-- ROADMAP -->
## Roadmap
<div id="Roadmap"></div>

- [x] Basic Functionality - Plot Graphs arranged on a page
- [x] Deploy on server
- [x] Basic Functionalities - Analytics, New Graph, Ai Chat
- [x] Advanced Analytics
- [x] Real Time RAY SQL DB 


<p align="right">(<a href="#top">back to top</a>)</p>
