# OIKOS: A FAMILY WEB ORGANIZER
#### Video Demo:  https://youtu.be/S-64B_fvhOU

#### Description:
This web app allows to visualize and keep track of the user agenda and also of the events in the agenda of the other family members in the user's family. It allows to add, remove and edit events and to associate them to one or more family members. This way, a general overview of the events planned for all the members of the family can be achieved.


## **Features**:
- Registration of new user.
- New user can choose to enter an **existing family** (if he knows the name) or to create a **new family**.
- Log in of user.
- Display monthly calendar with events for the user.
- Display container with daily events for user for current or selected date.
- Show details for selected daily event.
- Create new events for one or more family members.
- Edit event (if user is the event creator).
- Delete event (if user is the event creator).
- Display weekly agenda for all family members, with events displayed.
- Manage user's data.
- Log out.


## **Enviroment**:
This app is based on Python. It also uses SQLite for the app database and the Flask framework. Install python, Flask-SQLAlchemy (`pip install -U Flask-SQLAlchemy`), Flask-Migrate and Flask-Login with `pip install Flask-Migrate` and `pip install flask-login`. Also install Werkzeug with `pip install Werkzeug`. Start the app by running `python run.py`.  It will start Flask server and you can view the app by clickin at the adress. 

### **Project Organisation**:
The project folder contains the following folders and documents:
- README.md

- **app** Folder containing:
    - **routes** Folder containing:
        - **routes_event.py**: document for routes managing events.
        - **routes_index.py**: doc for main index route.
        - **routes_log.py**: doc for managing user log in, registration, and managing user data.

    - **static** Folder containing: *(here I got quite messy by organising the css formats. I am aware that I should have kept it better organized and that many documents contain redundant information, so it would have been better to distribute the formatting information in a smarter way using less number of documents and avoiding duplications)*.
        - **custom_calendar.css**: formatting of the calendar from FullCalendar.
        - **custom_createEvent.css**: formatting site for the route for creating new event.
        - **custom_login.css**: formatting site for the login route.
        - **custom_weekly_agenda**: formatting of the weekly agenda object.
        - **event_functions.js**: JavaScript document containing functions necessary for getting event and user information to be displayed or used in main.js or html documents. *(here I would rather change the name because it does not only contain functions related to events but also to user information)*.
        - **main.js**: JavaScript document containing the code for initializing and displaying the monthly calendar of the index route, by using the latest version of [FullCalendar](https://fullcalendar.io/).
        - **modal_script.js**: document containing script for the functions necessary for the modal window that contains the details of a selected daily event and the delete and editing functions.
        - **modal.css**: formatting of modal window.
        - **styles.css**: formatting of main index site.
        - **update_week.js**: script for functions implementing the weekly agenda displaying events for all the members of the family.

    - **templates**: Folder containing the html files of the app.

    - **__init__.py**: initialization of the app, also imports models and routes.

    - **forms.py**: contains code for the forms used in the app (log in, registration, edit, etc.).

    - **helpers.py**: document containing code for two "helper" functions: one for getting the days of the week in a list and the other for formatting floats or integers into EUR *(Not used, I thought of it for the implementation of a feature allowing members of the family to create a monthly or weekly budget and shopping lists)*.

    - **models.py**: code for the db.model classes and tables used in the database, also stablishing their relationships.

- **migrations**: this folder stores the history for the migrations in the database using Flask

- **venv**: enviroment.

- **app.db**: the SQL database.

- **config.py**: configuration of the app and the database.

- **run.py**: initialize and runs the app.


## **App design**:
After running and accesing the app, user is redirected to the log in route, where user can log in or register.
### **Registration**:
Registration is implemented in `routes_log.py`, by the `register()` function. We need to import the database `db` and the `app`, as well as the models for User and Family from `models.py`, also the `RegistrationForm` from `forms.py`. The Registration Flask form should be filled up be the new user. Some of the fields are optional, like 'Alias'. The email adress should be unique and not be registered by any other user, otherwise new user will be prompted to use other email address. New user can choose between entering an existing Family group or creating a New Family group.

After succesfully submitting the form, a the SQL database will be updated with a new user data, which will be associated to an existing or new Family. This mThe user will be redirected to the LogIn route.
### **LogIn**:
In `routes_log.py` we need to import the flask modules `flask` and `flask_login`, also `LoginForm`from `forms.py`.
User is prompted to fill the LogIn Flask form by entering the user name or email and the password. After succesfull log in, user will be remembered by `remember_me = BooleanField('Remember Me')` and redirected to the index home page `@app.route('/')`.
### **Index (home page)**:
Accesing the `index.html` page is restricted to logged users by `@login_required`. This site will display a wellcoming message to the user (by user name or alias if exists). Under this message, two buttons allow to access the `@app.route('/manage_user_data')` route for managing user data in `routes_log.py`  or to log out by `@app.route('/logout')`.

It also displays a monthly calendar implemented in `main.js` using [FullCalendar](https://fullcalendar.io/). A container placed under the calendar lists the user events for the selected date. The default date is current date. Several functions are implemented in the `event_functions.js` document, e.g., `fetchCurrentUserId()` for getting the userId, `fetchEventsforUser(userId)` for getting a list of dictionaries with the events and their information. These functions use AJAX to pass the function request to the corresponding route in `routes_event.py` in the server and then pass the information back, process it by JavaScript and updating the browser.

The container displaying user daily events for the selected date is created by the `createEventDiv(event, dailyEvents)`function defined in `event_functions.js`. Each event will display a different color deppending on their event class, also icons from [FontAwesome](https://fontawesome.com/). By clicking in the event, a **modal window** will open displaying the details for this event and buttons for redirecting user to the delete or edit event routes implemented in `routes_event.py`. If there are no events for the selected date, this the daily event container will display the corresponding message.

A button under the daily events container redirects user to the **create event** route implemented in `routes_event.py`. 

On the right side of the `index.html`, a container displays the name of the Family from which the user is member of and a table called `weekly-agenda` displaying the 7 consecutive days starting from the selected date in the monthly calendar (as rows) and columns for each member of the Family. The table shows the events for each member of the family in each of the 7 days. If user selects a new date, the table will be deleted and created againg with the data corresponding to the new selected date by the function `updateWeeklyAgenda(startDate)`implemented in `update_week.js`. *This was one of the most challenging tasks to implement. First, I get the family members of the user's family by the function `fetchFamilyUsers()`. Then I create the columns of the table (one of them for dates, the rest for the name of the family users). Then I have to iterate with a loop through every of the 7 days and retrieve the events for each user at the date of the loop, iterating through the list I got with the `fetchFamilyUsers()` function and creating the corresponding Event Block with some of the information of the event*. 

### **Create Event and Edit Event:**
The buttons for creating new event and edit an event redirect user to the respectives routes. The user can then fill the `EventForm(FlaskForm)`or `EditEventForm(FlaskForm)`. Some of the fields are compulsory like:
- Title
- Start date

It is possible to select one or more participants for the event within the members of the user's family. If no participants are selected, the default participant will be the current user.
It is possible to select the type of event from a given list (vacation, work, etc) or create a new type of event (which will be stored as a EventType(db.Model) in the database).
With the Edit Event form, the user can change the attributes of the event, but only if the current user was the creator of the event.

### **Manage User Data:**
Similarly, the route for managing use data allows user to change some of the user's data like the alias, the password or the email address.

### **DataBase Design:**

The app database has different classes of models and tables. For creating one to many or many to many relationship I use the method `db.relationship` and backref function, in the fashion of youtube series of videos from Codemy.com (here for one to many relationships: https://youtu.be/mwjrtntk0PE).
- class Family: many users can be part of a given family.
- class User: a user has to be associated to a family and can be associated to many events.
- class Event: an event can as well be associated to many users within a family, and can be associated to an event type.
- class EventType: a given event type can have many different events associated. 
- table `event_participants` for a many to many relationship between users and events.












