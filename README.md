# PartyPlanner Design Document

## Architecture

Describe the overall architecture of the application and technologies used (feel free to use
diagrams)

Overall, there will be 3 main components of the application: The app server, the database, and the
web interface. Each of these exist as a docker component in the development environment, but the
database and web interface would likely exist on their own as a managed service in production (e.g.
a dedicated PostGres server vs a postgres container).

The app server will be a django application which handles the business logic of the application. At
first, it will also render all of the web pages using it's own templating engine (Jinja2). I've
chosen to use Django, as I know it very well, and it allows for rapid prototyping of web
applications as it comes preconfigured with a lot of common functionality so development work can
focus on real business value. Note: The jinja-based UI will be very minimal - just something to let
me check that things are working.

The database is exactly what it sounds like - the persistent storage layer of the application. I'm
using Postgres because that happens to be the database technology with which I am most familiar. One
of the benefits of Django is that it abstracts the database just enough that it's not terribly
important which precise database technology is being used, so the database engine can theoretically
be changed if needed.

Lastly, the web interface is the 'entrypoint' into the application. It takes the form of an Nginx
server that controls access to the app server. initially, it'll just be a reverse-proxy to the
development app server, as that will be handling all of the UI elements. Later on, however, I will
rebuild the user interface with React. At this point, the web interface will then serve the react
app and allow the client-side app to communicate with the web app's API.

## Front-end Architecture

The application will have a number of Views, roughly equivalent to a web page, but not completely.
They are as follows:

- Sign up**
- Log in**
- Event List
- Create Event**
- Edit Event**
- Event Details
- Register for Event*
- Unregister from Event*

The last two(*) aren't quite fully functional pages, as they are simply actions. The user would
click a button on the event details page, which would make a request to the app server, after which
the user remains on the updated event details page. Four of these(**) require a form for the user to
fill out, but the create and edit event forms are going to be essentially the same. So 3 forms are
required:

- Sign up form
- Log in form
- Create/edit event form

Once I finish the no-react version of the application, I'll use that to determine the React
components that I'll need to implement in that version.

## Database Schemas

There are 3 main tables here: Users, Events, and Attendance.

![Database Schema Diagram](https://i.imgur.com/lAfqmNq.jpg)

A few things to note. Firstly, the 'password' field on the Users table does *not* contain the user's
plain-text password. It will be salted and hashed before storage, so that an attacker can't easily
access passwords with database access alone. The Attendance table tracks registration for an event.
It has a compound primary key between both it's user_id and event_id fields, ensuring that each
record has a unique combination. it also means that the mere existance of a record indicates whether
a user has registered for a given event, and it's absence means they have not done.
