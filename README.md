# calendar_manager
<img src="https://github.com/wsvincent/awesome-django/raw/main/assets/django-logo.svg">
<h2>Contents</h2>
<ul>
   <h3><a href="#info"><strong>Info</strong></a></h3><p>Information about the resources used in this project</p>
   <h3><a href="#django_calendar"><strong>CalendarManager</strong></a></h3><p>Social media site for managing business meetings and friends meeting</p>
   <h3><a href="#clone_project"><strong>Clone and Run a Django Project</strong></a></h3><p>how run projects in your computer</p>
</ul>
<hr>

<details><summary id="info" style="font-size: 30px;"> INFO</summary>
<h4>Information about the additional library, external Api used in this project and general information</h4>

<strong>Django</strong>
A high-level Python web framework that encourages rapid development and clean, pragmatic design..

<strong>Bootstrap</strong> Powerful, extensible, and feature-packed frontend toolkit.

<strong>django-widget-tweaks</strong> Tweak the form field rendering in templates, not in python-level form definitions. Altering CSS classes and HTML attributes is supported.

<strong>pytest-django</strong> pytest-django allows you to test your Django project/applications with the pytest testing tool.

<strong>django-storages/boto3</strong> django-storages is a collection of custom storage backends for Django.Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of services like Amazon S3 and Amazon EC2.

<strong>django-sslserver2</strong> Django package to support both HTTP and HTTPS as runserver command. (For testing social Autch )

<strong>social-auth-app-django</strong> This is the Django component of the python-social-auth ecosystem, it implements the needed functionality to integrate social-auth-core in a Django based project.

<strong>HTMX</strong> htmx gives you access to AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML, using attributes, so you can build modern user interfaces with the simplicity and power of hypertext

<strong>channels</strong> Channels is a project that takes Django and extends its abilities beyond HTTP - to handle WebSockets, chat protocols, IoT protocols, and more. It’s built on a Python specification called ASGI.

</details>

<hr>


<center><h1 id="django_calendar"> Calendar Manager <span style='font-size:80px;'><img src="https://img.icons8.com/doodle/48/null/apple-calendar--v2.png"/></span></h1></center>

## The website contains several applications:
* accounts
* calendar
* Chat app

<h3>Accounts</h3>

You must be register to have full access to all features. When creating a new profile, you need to select when you will be available for meetings from one hour to an hour, as well as the meeting format (it can be 15/30/45/60 minutes or one day) and the days of the week. All this information will be needed to count available seats and avoid booking when you are not available or physically unable to do so.

<img src="https://user-images.githubusercontent.com/97242088/221548589-58dfb309-ae79-42fd-a58e-e27e45d7f1f9.png" alt='Sign in'> <br>

*In app accounts I use HTMX to dynamically connect my views with backend. This is another way of communication between frontend and backend

<img src='https://user-images.githubusercontent.com/97242088/221548641-e442bd45-3fa3-440d-baf8-0e20e1be565a.png'  width='300' alt='Sign on'>

Without registering, you can view users, view the list of their appointments (if they have selected the scoupe calendar for "all"), but that's all you can do.

<img src='https://user-images.githubusercontent.com/97242088/225920454-3e77d14a-4075-4402-beb5-449596895bda.png'  alt='Register'>

You can go back to your profile settings and change anything at any time.

<h3>Calendar</h3>

After creating a new account, you now see your Calendar, nothing happens in it, but when you have an appointment, that appointment will appear in your calendar.

How your profile will be visible to others will depend on the settings in your profile. Full information may be available to all users, only friends or only you. Also when you select the "Organization" role in the settings, your profile and calendar will have a different view, but we'll talk about that later.

<img src='https://user-images.githubusercontent.com/97242088/225916137-cf20e681-9b4a-427e-aae2-e0af14920097.png'  alt='Calendar'>

Let's check someone's calendar.

When you visit someone else's calendar view, you can ask them for an appointment. However, you should check the time and day and availability, because if you choose the wrong time, you can send him this form, and of course, you can't ask him to meet you in the past.

<img src='https://user-images.githubusercontent.com/97242088/225927091-b88ca018-5576-4bbb-9d65-1a830551b9d3.png' alt='Meeting'>

As you can see, there is a difference between what the calendar looks like for its owner and what it looks like for a guest (if you are the owner you have more information about appointments).

<img src='https://user-images.githubusercontent.com/97242088/225927071-d6238e80-f3ef-45dd-93cb-b650eb7ef4f8.png' alt='Meeting2'>

If everything is correct, this user will see our request in his panel and only if he accepts it, the meeting will be in our calendar and in his. The number of vacancies in both our calendars will be recalculated.

<img src='https://user-images.githubusercontent.com/97242088/225916951-a4baa913-e164-464a-aa9c-f6984b37b2f9.png' alt='meeting ok'>

If he ignores it, the meeting will go down in history, but it won't affect anything.

You can follow users and users can follow you. In the search input, enter a username, last name or nickname and find him.

<img src='https://user-images.githubusercontent.com/97242088/225916409-a00662a7-fef2-406a-9738-eb802c2a954a.png'>


<h3>Chat Rooms</h3>

The "Chat" application creates a WebSocket connection between users in their room. 

*I use Django channels for this.

I call it rooms, but in my app it's called "discussions". If the user is online (it means they have an open dialog) this discussion will have a green point.

<img src='https://user-images.githubusercontent.com/97242088/226368965-983b52ba-ca50-44cd-b8e7-7e85ecb37c1b.png'>

In the dialog view, all users will have the same view at the same time (you don't need to reload the page to see new messages)

<img src='https://user-images.githubusercontent.com/97242088/225919195-7bdd33bc-ae42-41af-97e5-e498d2c40f78.png'>

If you want, you can rename the room and add more users to the discussion.


*this page is not finished yet

<center><h2 id="clone_project">Clone and Run a Django Project</h2></center>

Before diving let’s look at the things we are required to install in our system.

To run Django prefer to use the Virtual Environment

`pip install virtualenv`

Making and Activating the Virtual Environment:-

`python -m venv “name as you like”`

`source env/bin/activate`

Installing Django:-

`pip install django`

Now, we need to clone project from Github:-
<p>Above the list of files, click Code.</p>
<img src="https://docs.github.com/assets/cb-20363/images/help/repository/code-button.png">

Copy the URL for the repository.
<ul>
<li>To clone the repository using HTTPS, under "HTTPS", click</li>
<li>To clone the repository using an SSH key, including a certificate issued by your organization's SSH certificate authority, click SSH, then click</li>
<li>To clone a repository using GitHub CLI, click GitHub CLI, then click</li>
</ul>
<img src="https://docs.github.com/assets/cb-33207/images/help/repository/https-url-clone-cli.png">

Open Terminal.

Change the current working directory to the location where you want the cloned directory.

Type git clone, and then paste the URL you copied earlier.

`$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY`

Press Enter to create your local clone.

```
$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
> Cloning into `Spoon-Knife`...<br>
> remote: Counting objects: 10, done.
> remote: Compressing objects: 100% (8/8), done.
> remove: Total 10 (delta 1), reused 10 (delta 1)
> Unpacking objects: 100% (10/10), done.
```

Install the project dependencies:

`pip install -r requirements.txt`

create .env file,
put this information in file.

```python
DEBUG=True 
SECRET_KEY='your_secret'

POSTGRES_DB='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'

AWS_ACCESS_KEY_ID='your_id'
AWS_SECRET_ACCESS_KEY='your_key'
AWS_STORAGE_BUCKET_NAME='your_bucket_name'


AWS_S3_FILE_OVERWRITE=False

SOCIAL_AUTH_FACEBOOK_KEY="your_facebook_appid"
SOCIAL_AUTH_FACEBOOK_SECRET="your_facebook_secretkey"
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY="your_google_key"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET="Your_google_secret"

EMAIL_HOST_USER='email'
EMAIL_HOST_PASSWORD='app-pasword'
```

!!!! If you want to use all the features of this site, you should first create a bucket in amazon C3, create development pages in google, facebook and set up your mail account !!!

create admin account (**remember you must be at the main application folder with file manage.py, and do this steps for
each application in this repository!!!!**)

`python manage.py createsuperuser`

then

`python manage.py makemigrations`

then run

`python manage.py migrate`


to start the development server

`python manage.py runserver`

and open localhost:8000 on your browser to view the app.

run tests

```
   > cd tests
   > pytest
```

<img src='https://user-images.githubusercontent.com/97242088/226597366-04d7370b-1ec0-4180-b2a7-3bb0716cc7aa.png'>

Have fun
<p style="font-size:100px">&#129409;</p>