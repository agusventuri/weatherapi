# weatherapi
This small piece of code is my solution to the code challenge provided by Globant while applying for a Python developer position.

Here you can find an api that takes two parameters as input for its only endpoint and produces, if able, a weather forecast formatted in a friendly way, using openweather as it's source of information.
It consist of two parts, a backend that takes the input and searches openweather for the information and a frontend that takes the answer and displays it.

To run it you need an enviroment with python 3, flask and some other libraries. You can install them with pip using the requirements file. 
Assuming you're on Linux, open your terminal and head to the directory where you have the project. Then run the following commands:
```
export FLASK_APP=weatherapi
export FLASK_SECRET_KEY=[your_secret_key]
export OPENWEATHERMAP_APPID=[your_openweather_appid]
run flask
```
Remember to replace the flask secret with a secret of your choosing and the openweather appid with the one provided by openweather.
Without this information the project cannot run.

After running this commands you can head to http://127.0.0.1:5000/ and search for a city accompanied with a 2-character country code

You can explore the API thanks to swagger. Just head to http://127.0.0.1:5000/api/docs/

You can also test the endpoint with a tool like Postman. The endpoint is like follows
```
GET /weather?city=$City&country=$Country&
```
You can test with this example:
http://127.0.0.1:5000/weather?city=toronto&country=ca

To test this app, you can run `pytest` inside weatherapi's root directory.

