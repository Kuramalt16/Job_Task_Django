# Job_Task_Django
To run the app install the requirements:

	pip install -r requirements.txt
 
once installed install Redis through this link:

	https://github.com/tporadowski/redis/releases

once Redis has been installed on your computer (usualy in the program files) run "redis-cli.exe" and type "ping",
if recieved "PONG" Redis is running correctly
 
next in your terminal run "py manage.py runserver" this launches the server which you can access by typing in the 
url in your web browser "localhost:8000".

Alternatively you can choose a diferent port by running "py manage.py runserver [PORT]" 
example: "py manage.py runserver 9000" and then access the website through the url "localhost:9000".

Once the webserver is running you are greeted in the homepage. You can navigate to the About page for information about me and the project. 
Or you can click on the last icon which will take you to the application for managing finances. 
You will again have to choose an option, view the list of the existing companies or add your own company.

The list of the companies shows real time data of companies current:
* Open Price: This is the price at which a stock begins trading when the market opens for the day. It's the first transaction price of the day.
* Previous Close Price: This is the price at which the stock traded at the end of the previous trading session. It's essentially the closing price of the stock from the last trading day.
* Day High: This is the highest price at which the stock has traded during the current trading day. It reflects the peak value the stock reached since the market opened.
* Day Low: This is the lowest price at which the stock has traded during the current trading day. It represents the lowest value the stock has reached since the market opened.
* Volume: This is the daily average of shares or contracts traded. It indicates the level of market activity for a particular stock or asset within that timeframe.

It is possible to click on a company's ticker and have the data visualized in a form view, update the data, export it, or delete it.

Once chosen to add a new company to the list you are required to provide a ticker which the yfinance library will use to find the company's data and present it to the user in the table. 
If the chosen ticker does not exist in the yfinance library, the user will be prompted with a message that indicates the use of an invalid ticker.
