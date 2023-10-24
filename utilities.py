import random

# Random number between x and y
def GetRandInt(num1, num2):
    return random.randint(num1, num2)



# Weather
def GetCelsius(num):
    global weatherType
    weatherType = ''
    celsius = (num - 273.15)

    if celsius < 18:
        weatherType = 'cold'
    elif celsius < 24:
        weatherType = 'normal'
    else:
        weatherType = 'hot'

    return celsius

def GetFahrenheit(num):
    fahrenheit = (GetCelsius(num) * (9/5) + 32)
    return fahrenheit

def GetWeatherType():
    return weatherType



# Time
import time

def GetSysTime():
    curHours = time.strftime('%H:%M:%S')

    return curHours

def GetSysDate():
    date = time.strftime('%d/%m/%Y')

    return date
