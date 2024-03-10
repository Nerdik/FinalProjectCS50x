# WeatherBot
### [Video Demo](<https://youtu.be/jSLrlbJ5EM4>)
### Description
#### Main abilities
This is the Telegram bot which shows the weather forecast for the most cities of the world. The user have ability to choose the day or period: today, tomorrow or the following week.
#### Main structure
The main Telegram functionality is based on [pyTelegramBotAPI](<https://pypi.org/project/pyTelegramBotAPI/>) package.

The program code consists of two files ```telegram.py``` and  ```helpers.py```.

```telegram.py``` includes 6 perfoming functions```tele_start_func()```, ```tele_get_city()```, ```tele_get_city_2()```, ```tele_get_date()```, ```tele_get_date_func()```, ```output()```.

```helpers.py``` includes 3 perfoming functions ```get_city()```, ```get_weather()```, ```get_coordinates()```.

#### Details of ```telegram.py``` functioning
```tele_start_func()``` - the function greets the user and prompts the user to input the name of the city for weather forecast and initiates ```tele_get_city()``` function.

```tele_get_city()```, ```tele_get_city_2()``` - the function gets as initial data the name of the city and checks it with ```helpers.get_city()```. If the name of the city doesn't fit the database or the name was typed incorrectly the function ```tele_get_city()``` prompts to try to type the name of the city again and launches ```tele_get_city_2()```. If the name of the city doesn't fit again ```tele_get_city_2()``` launches ```tele_get_city()```. After the checking procedure succeed the function puts the city name into the ```database``` (dictionary) with the key ```chat.id``` in order to serve many users at the same time.

```tele_get_date()``` - the function prompts the user to choose the date/period for the forecast by pushing one suggested button: ```Today```, ```Tomorrow```, ```Week``` and initiates next processing function ```tele_get_date_func```.

```tele_get_date_func()``` - the function processes ```callback_data``` from ```tele_get_date()``` and puts into the ```database``` (dictionary) with the key ```chat.id``` the list of dates. For ```Today``` - today date, for ```Tomorrow``` - tomorrow date, for ```Week``` - 7 dates for each of 7 following days. The format is ```'YYYY-MM-DD'```.

```output()``` - the function gets as initial data the valid city name, date/period, latitude/longitude with ```helpers.get_coordinates()```, weather parameters with ```helpers.get_weather()```. The function makes an output form and then prints it. If choice of the user is ```Today``` or ```Tomorrow``` it prints the following form:
```
City name

Date

Min temperature: _°C
Max temperature: _°C
Precipitation: _mm
```
If choice of the user is ```Week``` the function prints the following form:
```
City name

Date1
Temperature: _°C

Date2
Temperature: _°C

Date3
Temperature: _°C

Date4
Temperature: _°C

Date5
Temperature: _°C

Date6
Temperature: _°C

Date7
Temperature: _°C
```


#### Details of ```helpers.py``` functioning


```get_city()``` - the function gets as initial data the name of the city (case fold insensitive) and then checks if it is in database of the open weather source [open-meteo.com]. If there is no answer from the source, the function prompts to try later. If the name of the city doesn't fit the database or the name was typed incorrectly the function prompts to try to type the name of the city again. After the checking procedure succeed the function returns the valid name of the city.   


```get_coordinates()``` - the function gets as initial data the valid name of the city and then requests the coordinates of chosen city from the open source [open-meteo.com]. If there is no answer from the source, the function prompts to try later. After the process of receiving answer from the source succeed the function returns the list which contains coordinates: latitude and longitude.

```get_weather()``` - the function gets as initial data the date and coordinates of the city. The function makes a request to the open source [open-meteo.com] and receives the following data: daily maximum temperature in Celsius, daily minimum temperature in Celsius, and daily precipitation in mm. After getting the response the function returns the list which consists of maximum temperature, minimum temperature and precipitation.

### TODO
#### Before start
Install package Requests
```
pip install requests
```
and package pyTelegramBotAPI
```
pip install pyTelegramBotAPI
```
Or instead you can use the following
```
pip install -r requirements.txt
```
#### Usage
Run the program with the main file ```telegram.py``` using following
```
python telegram.py
```
or other methods according to your system.

[!NOTE] The user must have acsess to the internet for the proper usage of the program.
