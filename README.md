# Cyber Security MOOC Project I

## Introduction

This project has been built for the course [Cyber Security Base MOOC](https://cybersecuritybase.mooc.fi/). Please note that the code includes intentional security flaws so use at your own risk. The course task was to build a web application that has different security flaws from the OWASP top 10 security list. The flaws are described below.

Moodtracker is a simple web application that allows you to measure your happiness and displays your results on a chart.

## Project report

Unless otherwise stated, the code line refers to views.py file.

### How to get started

- Clone the directory with git clone
- Create a new virtual environment for the project with python3 -m venv
- Activate the virtual environment you just created
- Install required packaged with

        pip install -r requirements.txt

- Make sure the database is initialized

        python manage.py migrate

- Start the server with

        python manage.py runserver

- Go to

        localhost:8000/moodtracker/

### #1 Broken Access Control

Access Control policies should make sure that user cannot perform any actions or access any resources outside their intended permissions.

In this application, unauthorized user can access views they should not be able to access by modifying the URL. Start the application,  modify the url for example to ../moodtracker/rate.

If user is not logged in, they should not be able to access results or rating page. At the moment, results page does not show any user data if the user is not logged in but it shows an empty chart. If the user uses the rating page and submits the form it will lead to an error and the application stops working correctly. 

The solution is to use Django's login_required decorator. It will limit access to the page if the user is not logged in and redirect the user to the login page. 

Solution on [line 22](https://github.com/ellisrnm/hy-cybersec-2022/blob/main/moodtracker/views.py#L22) and [line 37](https://github.com/ellisrnm/hy-cybersec-2022/blob/main/moodtracker/views.py#L37).

### #2 Identification and Authentication Failures

The application should be designed so that it protects from authentication-related attacks. Currently, there are authentication weaknesses since there are no validation when user creates an account.

When an user registers a new account to the application, the user is created with Django's User.objects.create_user() on [lines 93-94](https://github.com/ellisrnm/hy-cybersec-2022/blob/main/moodtracker/views.py#L93-L94) where password validation is not applied.

The application does not allow empty strings as usernames but anything else passes such as " ". The application allows very poor passwords such as "password" or the same as the username, and it even allows empty passwords as there is no validation. The app is not protected from automated attacks and brute forcing login attemps.

I could write some general checks for the username and password similarly than on [lines 83-86](https://github.com/ellisrnm/hy-cybersec-2022/blob/main/moodtracker/views.py#L83-L86) here. A better idea would be to use Django's validators. There is a function in django.contrib.auth.password_validation that validates a password: validate_password. Then the password validation needs to be enabled and configured in the settings which is already true. These validators will check common cases such as too short passwords, passwords too similar to username or too common passwords. Validate_password function used on [lines 87-92](https://github.com/ellisrnm/hy-cybersec-2022/blob/main/moodtracker/views.py#L87-L92).

### #3 SQL Injection

SQL injection is a common attack when the attacker uses malicious SQL code to manipulate the database in the backend. It can be used for example to delete entries or access information.

In this project, I have intentionally used a raw SQL query that is vulnerable to attacks. The code really makes no sense and I had to write additional steps that are not beneficial. It looks horrible but I had to do quite some effort to go past Django's SQL injection mitigation efforts. :) It was for the sake of showing that SQL injection is possible. The bad part of the code can be found from [lines 58-64](https://github.com/ellisrnm/hy-cybersec-2022/blob/main/moodtracker/views.py#L58-L64). The executescript function and the poorly written SQL statement allows the SQL injection [lines 58-60](https://github.com/ellisrnm/hy-cybersec-2022/blob/main/moodtracker/views.py#L58-L60). So start the application, login and make sure there are some ratings showing in the results page. Then logout, go to login page, and try the following as the username:

    a"; DELETE FROM moodtracker_mood; --

The application will show you an error message _Something went wrong_. If you now login with real credentials you will notice that all the previous ratings are gone.

The solution is to use ORM so in this case Django's built-in QuerySet API instead. If raw queries are needed, the inputs should be parameterized. In this case, I have provided the solution in the [lines 67-70](https://github.com/ellisrnm/hy-cybersec-2022/blob/main/moodtracker/views.py#L67-L70) by using QuerySet API because it's the safest and also removes all the additional steps from the code.

### #4 Cross-site Scripting

XSS vulnerabilities allow users to include malicious content to a site.

By default, Django projects applications from XSS vulnerabilites by escaping specific characters in templates. In this exercise, I have used _safe_ template tag that marks a string not requiring escaping. This allows the user to use XSS attacks. The issue is on the [line 7](https://github.com/ellisrnm/hy-cybersec-2022/blob/main/moodtracker/templates/moodtracker/login.html#L7) in login template.

So start the application and register a new user with the following username:

    <script>alert('Hacked');</script>

Then modify the URL and go to login page ../moodtracker/login (make sure you are already logged in). You can see the alert on the page instead of your username as a string.

This issue can be fixed by removing the _safe_ tag from the row. Then it will show your username as a string instead. A correct example can be found from register template on [line 7](https://github.com/ellisrnm/hy-cybersec-2022/blob/main/moodtracker/templates/moodtracker/register.html#L7). You can check how it should look like by going to register page using the URL ../moodtracker/register while logged in.

### #5 Cross Site Request Forgery

CSRF is a common vulnerability that allows sending requests from another site. Django includes CSRF defence by default. If a form does not include {% csrf_token %}, the application will throw an error. For this project, I have marked _rate_ view as being exempt from the protection, [line 23](https://github.com/ellisrnm/hy-cybersec-2022/blob/main/moodtracker/views.py#L23). Now as the form sends a rating to server, csrf token is not included in rate template on [line 13](https://github.com/ellisrnm/hy-cybersec-2022/blob/main/moodtracker/templates/moodtracker/rate.html#L13). 

This problem is easily fixed by adding the csrf_token back to the form and by removing the csrf_exempt. 

### Extra

Settings.py includes options that should never be put to production and information that should not be published on version control.
