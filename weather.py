# Weather App
# Copyright (c) 2023, Jignas Paturu

from datetime import datetime
import json
from urllib import request
from pathlib import Path
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty
from kivy.config import Config

Config.set('graphics', 'resizable', False)


#######################################################################

class API():
    DATA = [{

        'city': 'City',
        'visibility': 0000,
        'zip': 560043,
        'country': 'in',

        'we_main': 'Clouds',
        'we_description': 'clear skys',
        'Icon': None,

        'temp': 101.0,
        'temp_min': 000.0,
        'temp_max': 00.0,
        'feels_Like': 00.0,
        'humidity': 0,
        'pressure': 0,

        'speed': 0.0,
        'deg': 0,

        'sunrise': 0000000000,
        'sunset': 0000000000,
        'utc_offset':000,

    }]

####################################################################################

    ip_req = request.urlopen("https://ipapi.co/json")
    ip_data = json.loads(ip_req.read())

    DATA[0]['city'] = ip_data['city'].title()
    DATA[0]['country'] = ip_data['country_code']
    DATA[0]['zip'] = ip_data['postal']
    DATA[0]['utc_offset'] = int( ip_data['utc_offset'])

    API_KEY = "732833a34bdd944fb2477423de2a2473"

    temp_a= f"http://api.openweathermap.org/data/2.5/weather?zip={DATA[0]['zip']},{DATA[0]['country']}&appid={API_KEY}"
    print("link=",temp_a)
    response = request.urlopen(
        f"http://api.openweathermap.org/data/2.5/weather?zip={DATA[0]['zip']},{DATA[0]['country']}&appid={API_KEY}")
    resp_data = json.loads(response.read())

##################################################################################

    DATA[0]['visibility'] = resp_data['visibility']

    DATA[0]['we_main'] = resp_data['weather'][0]['main']
    DATA[0]['we_description'] = resp_data['weather'][0]['description']
    DATA[0]['we_description']=DATA[0]['we_description'].capitalize()
    DATA[0]['Icon'] = resp_data['weather'][0]['icon']

    DATA[0]['temp'] = resp_data['main']['temp']
    DATA[0]['temp_min'] = resp_data['main']['temp_min']
    DATA[0]['temp_max'] = resp_data['main']['temp_max']
    DATA[0]['feels_Like'] = resp_data['main']['feels_like']
    DATA[0]['humidity'] = resp_data['main']['humidity']
    DATA[0]['pressure'] = resp_data['main']['pressure']

    DATA[0]['speed'] = resp_data['wind']['speed']
    DATA[0]['deg'] = resp_data['wind']['deg']

    DATA[0]['sunrise'] = resp_data['sys']['sunrise']
    DATA[0]['sunset'] = resp_data['sys']['sunset']

    print("rise", DATA[0]['sunrise'])
    print("set", DATA[0]['sunset'])


###################################################################

    cel=272.15

    print("utc_rise",datetime.utcfromtimestamp(DATA[0]['sunrise']))


    NEW_DATA = [{

        'time_sunrise': datetime.utcfromtimestamp(DATA[0]['sunrise']+36*DATA[0]['utc_offset']),
        'time_sunset': datetime.utcfromtimestamp(DATA[0]['sunset'] + 36 * DATA[0]['utc_offset']),

        'icon': f"http://openweathermap.org/img/wn/{DATA[0]['Icon']}@2x.png",

        'temp': round(DATA[0]['temp'] - cel) ,
        'temp_min': round(DATA[0]['temp_min'] - cel),
        'temp_max': round(DATA[0]['temp_max'] - cel),
        'wind_dir':""
    }]


###################################################################

# Wind Direction

    if (22.5< DATA[0]['deg']<67.5):
        NEW_DATA[0]['wind_dir'] = 'NE'

    elif (DATA[0]['deg']<=112.5):
        NEW_DATA[0]['wind_dir'] = 'E '

    elif (DATA[0]['deg']<=157.5):
        NEW_DATA[0]['wind_dir'] = 'SE'

    elif (DATA[0]['deg']<=202.5):
        NEW_DATA[0]['wind_dir'] = 'S '

    elif (DATA[0]['deg']<=247.5):
        NEW_DATA[0]['wind_dir'] = 'SW'

    elif (DATA[0]['deg']<=292.5):
        NEW_DATA[0]['wind_dir'] = 'W '

    elif (DATA[0]['deg']<=337.5):
        NEW_DATA[0]['wind_dir'] = 'NW'

    else:
        NEW_DATA[0]['wind_dir'] = 'N '


#####################################################################



    # icon_url = "http://openweathermap.org/img/wn/{}@2x.png".format(resp_data['weather'][0]['icon'])


    cur_time =int(datetime.now().timestamp())+36*DATA[0]['utc_offset']

    minus= DATA[0]['sunset']+36*DATA[0]['utc_offset']-1500
    plus = DATA[0]['sunset'] + 36 * DATA[0]['utc_offset'] + 1500
    if (DATA[0]['Icon']=='02d'):
        DATA[0]['Icon'] ='01d'

    if (DATA[0]['Icon']=='03d'):
        DATA[0]['Icon'] ='01d'

    if (DATA[0]['Icon']=='04d'):
        DATA[0]['Icon'] ='01d'


    if (DATA[0]['Icon']=='02n'):
        DATA[0]['Icon'] ='01n'

    if (DATA[0]['Icon']=='03n'):
        DATA[0]['Icon'] ='01n'

    if (DATA[0]['Icon']=='04n'):
        DATA[0]['Icon'] ='01n'

    if (DATA[0]['Icon']=='11d'):
        DATA[0]['Icon'] ='10d'

    if (DATA[0]['Icon']=='11n'):
        DATA[0]['Icon'] ='10n'

    if (DATA[0]['Icon']=='09d'):
        DATA[0]['Icon'] ='10d'

    if (DATA[0]['Icon']=='09n'):
        DATA[0]['Icon'] ='10n'

    print(minus,cur_time,plus)

    if ( minus< cur_time < plus):
        DATA[0]['Icon'] = 'sunset'

    print(DATA)
    print(NEW_DATA)

#############################

    testt= datetime.utcfromtimestamp(DATA[0]['sunrise']+36*DATA[0]['utc_offset'])
    print("timeeeee",testt)
    print("timeeeee",datetime.utcfromtimestamp(DATA[0]['sunrise']+36*DATA[0]['utc_offset']-3000))
#################################################################################

class Weather(App):

    ui_data= ListProperty(API.DATA)
    ui_newdata = ListProperty(API.NEW_DATA)
    a=API.DATA[0]['Icon']

    sky = Path(f"sky/{API.DATA[0]['Icon']}.png")
    hill = Path(f"hills/{API.DATA[0]['Icon']}.png")


    def build(self):
        return FloatLayout()


#######################################################################################
    
if __name__ == '__main__':
    API()
    Weather().run()


#####################################################################################
