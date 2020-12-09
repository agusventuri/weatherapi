# weatherapi
This small piece of code is my solution to the code challenge provided by Globant while applying for a Python developer position.

Here you can find an api that takes two parameters as input for its only endpoint and produces, if able, a weather forecast formatted in a friendly way, using openweather as it's source of information.
It consist of two parts, a backend that takes the input and searches openweather for the information and a frontend that takes the answer and displays it.

To run it you need an enviroment with python 3, flask and bootstrap. 
Assuming you're on Linux, open your terminal and head to the directory where you have the projecto. Then run the following commands:
```
export FLASK_APP=weatherapi
run flask
```

If I have the time I'll create a dockerfile to make it easier to run this.

