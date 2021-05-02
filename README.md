# Comics Management Website

Comics Management Website is a web application to manage the comic book subscriptions of any comic book store that works with the Previews system (you can check out this link here if you don't know what the Previews system is: [What is PREVIEWS?](https://www.previewsworld.com/Article/166508-What-is-PREVIEWS)). The website has its own database with clients, all the series that are being published and a system to start and stop subscriptions for any client in the database. 

## Installation

Clone the following Git Repository: https://github.com/iriverom/ComicsManagement


Do a poetry install.
If the Database is empty, create an admin by creating a superuser and run the file script.py to populate the database. (At the moment, and only for testing purposes, the database is also included in the git repository filed with fake client data). 

```bash
poetry install
```
If database is empty:
```bash
cd comics
python manage.py createsuperuser  
cd app
python script.py
```

## Usage

After having created a superuser, you can just start the server and open the address provided by the server in your browser of choice. Since the project is at an early state, to ensure maximum compatibility, a desktop with Firefox or Chrome is recommended.

```bash
python manage.py runserver
```
![Dashboard Screenshot]("dashboard_screenshot.JPG")

After you have succesfully logged in, the dashboard will open. Here you can see a simple overview of the state of the data with two graphs: one with the top 10 Series by number of clients subscribed and another one with how many customers have how many subscriptions. 

From the navbar you can then check all different possibilities of the website:

The **Client Table** the personal information of the clients is displayed and the user can remove the client and access their subscriptions. Subscriptions can be added or stopped.

In the **Series Table** the user can see which clients are subscribed to each Series.

The button **Export Order Form** generates an excel file with the comics that have to be ordered from the distributor according to the subscriptions giving the amount of comics and the total price per series. If more than one issue of a series is published in a given month all are also included.

The **Search bar** can be used for both clients and series. 

## License

This project is not open-source.

This project uses Bootstrap, Font Awesome, Chartjs


Comic book images are free of copyright. They were downloaded from [Comic Book Plus](https://comicbookplus.com/), an amazing website, where you can read and download thousands of comics that are public domain. 