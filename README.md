# Travel website
This is my first app on the Flask learning course.
I make travel site, that offers some nice tours from several towns. Small site for 3 or more pages.

Using dependencies: Flask, bootstrap 4, weather API OpenWeatherMap and no database.

The site has:

* '/' - main page (jumbotron and 6 random tours);
* '/data/departures/<departure>/' - page with tours from a certain town;
* '/data/tours/<tour_id>/' - page of a certain tour (with buy-tour button, i don't know yet how to make payment stuff);

< 🔻 *in progress* 🔻 >
* '/admin/' - admin's page with logging in for creating/editing/deleting tours; #TODO
* '/data/all/' - page with all tours; #TODO

Anyway you could run this app through [Heroku](<https://www.heroku.com>), just upload this repository there. (gunicorn and Procfile are already inclusive)
