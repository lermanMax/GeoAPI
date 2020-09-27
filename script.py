#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, make_response, request, abort 
app = Flask(__name__)  

path_to_RUbase = 'RU.txt'

'''
geonameid         :0 integer id of record in geonames database
name              :1 name of geographical point (utf8) varchar(200)
asciiname         :2 name in plain ascii characters, varchar(200)
alternatenames    :3 alternatenames, comma separated
latitude          :4 latitude in decimal degrees (wgs84)
longitude         :5 longitude in decimal degrees (wgs84)
feature class     :6 see http://www.geonames.org/export/codes.html, char(1)
feature code      :7 see http://www.geonames.org/export/codes.html, varchar(10)
country code      :8 ISO-3166 2-letter country code, 2 characters
cc2               :9 alternate country codes, comma separated
admin1 code       :10 fipscode
admin2 code       :11 code for the second administrative division 
admin3 code       :12 code for third level administrative division, varchar(20)
admin4 code       :13 code for fourth level administrative division, varchar(20)
population        :14 bigint (8 byte int) 
elevation         :15 in meters, integer
dem               :16 digital elevation model
timezone          :17 the iana timezone id (see file timeZone.txt) varchar(40)
modification date :18 date of last modification in yyyy-MM-dd format

feature classes:
A: country, state, region,...
H: stream, lake, ...
L: parks,area, ...
P: city, village,...
R: road, railroad 
S: spot, building, farm
T: mountain,hill,rock,... 
U: undersea
V: forest,heath,...
'''

keys_of_fields = [
        'geonameid',         
        'name',       
        'asciiname',         
        'alternatenames',    
        'latitude',          
        'longitude',         
        'feature class',     
        'feature code',      
        'country code',      
        'cc2',               
        'admin1 code',      
        'admin2 code',       
        'admin3 code',    
        'admin4 code',     
        'population',     
        'elevation',        
        'dem',             
        'timezone',         
        'modification date'
]

class_P = 'P' #city, village,...

RUtimeZones = { #TimezoneID : rawOffset (independant of DST)          
        'Asia/Anadyr': 12.0 ,
        'Asia/Barnaul': 7.0 ,
        'Asia/Chita': 9.0 ,
        'Asia/Irkutsk': 8.0 ,
        'Asia/Kamchatka': 12.0 ,
        'Asia/Khandyga': 9.0 ,
        'Asia/Krasnoyarsk': 7.0 ,
        'Asia/Magadan': 11.0 ,
        'Asia/Novokuznetsk': 7.0 ,
        'Asia/Novosibirsk': 7.0 ,
        'Asia/Omsk': 6.0 ,
        'Asia/Sakhalin': 11.0 ,
        'Asia/Srednekolymsk': 11.0 ,
        'Asia/Tomsk': 7.0 ,
        'Asia/Ust-Nera': 10.0 ,
        'Asia/Vladivostok': 10.0 ,
        'Asia/Yakutsk': 9.0 ,
        'Asia/Yekaterinburg': 5.0 ,
        'Europe/Astrakhan': 4.0 ,
        'Europe/Kaliningrad': 2.0 ,
        'Europe/Kirov': 3.0 ,
        'Europe/Moscow': 3.0 ,
        'Europe/Samara': 4.0 ,
        'Europe/Saratov': 4.0 ,
        'Europe/Simferopol': 3.0 ,
        'Europe/Ulyanovsk': 4.0 ,
        'Europe/Volgograd': 4.0
}


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

def fields_to_dict(necessary_fields):
    
    for i in [0,14,15]: 
        if necessary_fields[i].isdigit(): 
            necessary_fields[i] = int(necessary_fields[i]) # id, population, elevation should be integer
            
    for i in [4,5]: 
        necessary_fields[i] = float(necessary_fields[i]) # latitude, longitude should be float
    
    return dict(zip(keys_of_fields, necessary_fields))


@app.route('/findCityByID', methods=["GET"]) 
def find_city_by_id():
#    path_for_geobase = request.json.get('path_for_geobase', path_to_RUbase) # the ability to select a database
    path_for_geobase = path_to_RUbase
    
    if not request.json or not 'geonameid' in request.json: abort(400)
    if type(request.json['geonameid']) is not int: 
        return make_response(jsonify({'error': 'geonameid is not integer'}), 400)
    
    necessary_fields = []
    
    with open( path_for_geobase, 'r') as geobase:
        for line in geobase:
            fields = line.strip().split('\t')   
            if int(fields[0]) == request.json['geonameid']:
                necessary_fields = fields
                break
            
    if not necessary_fields : #list is false if empty  
        return make_response(jsonify({'error': 'This id not found in this database'}), 404)
    
    elif necessary_fields[6] != class_P:
        return make_response(jsonify({'error': 'It is not a city'}), 400) 
    
    return jsonify(fields_to_dict(necessary_fields)) 
        

def find_city_by_name(name, path_for_geobase = path_to_RUbase):
    
    if type(name) is not str: 
        return make_response(jsonify({'error': 'name is not string'}), 400)
    
    necessary_fields = []
    max_population = 0
    
    with open( path_for_geobase, 'r') as geobase:
        for line in geobase:
            fields = line.strip().split('\t')
            alternatenames = fields[3].split(',')
            if fields[6] == class_P and name in alternatenames and int(fields[14]) > max_population :
                necessary_fields = fields
                max_population = int(fields[14])
            
            
    if not necessary_fields : #list is false if empty  
        return make_response(jsonify({'error': 'This city not found in this database'}), 404)
    
    return fields_to_dict(necessary_fields)
    

@app.route('/compareTwoCities', methods=["GET"]) 
def compare_two_cities():
#    path_for_geobase = request.json.get('path_for_geobase', path_to_RUbase) # the ability to select a database
    path_for_geobase = path_to_RUbase
    
    if not request.json or not 'name_1' in request.json or not 'name_2' in request.json: abort(400)
    
    compare = {
            'city_1': find_city_by_name( request.json['name_1'], path_for_geobase),
            'city_2': find_city_by_name( request.json['name_2'], path_for_geobase),
            'which_north': None, # name of city which is farther north. 'None' if these have the same latitude
            'same_timezone': True, # 'True' if cities have the same timezone 
            'difference_time': 0
            }
    
    
    if type(compare['city_1']) is not dict: return compare['city_1'] # if it is not dict then it is error
    if type(compare['city_2']) is not dict: return compare['city_2'] # if it is not dict then it is error
    
    if float(compare['city_1']['latitude']) > float(compare['city_2']['latitude']): 
        compare['which_north'] = request.json['name_1']
    elif float(compare['city_1']['latitude']) < float(compare['city_2']['latitude']): 
        compare['which_north'] = request.json['name_2']
    
    if compare['city_1']['timezone'] != compare['city_2']['timezone']: 
        compare['same_timezone'] = False
        compare['difference_time'] = RUtimeZones[compare['city_2']['timezone']]-RUtimeZones[compare['city_1']['timezone']]
    
    return jsonify(compare)


@app.route('/pageOfCities', methods=["GET"])  
def page_of_cities() :
#    path_for_geobase = request.json.get('path_for_geobase', path_to_RUbase) # the ability to select a database
    path_for_geobase = path_to_RUbase    
    
    if not request.json or not 'page' in request.json or not 'count' in request.json: abort(400)
    
    if type(request.json['page']) is not int: 
        return make_response(jsonify({'error': 'page is not integer'}), 400)
    if type(request.json['count']) is not int: 
        return make_response(jsonify({'error': 'count is not integer'}), 400)
    if request.json['page'] < 1 or request.json['count'] < 1: 
        return make_response(jsonify({'error': 'page or count is less than one'}), 400) 
    
    necessary_list = []
    
    N_first= (request.json['page']-1)*request.json['count'] + 1 # number of the first city on this page
    N_last = request.json['page'] * request.json['count'] # number of the last city on this page
    
    with open( path_for_geobase, 'r') as geobase:
        n = 0 # counter of cyties in base 
        for line in geobase:
            fields = line.strip().split('\t')
            if fields[6] == class_P:
                n+=1 
                if n >= N_first: necessary_list.append(fields_to_dict(fields))
                if n >= N_last: break
    
    if not necessary_list: #list is false if empty  
        return make_response(jsonify({'error': 'this page is empty' }), 404)
            
    return jsonify(necessary_list) 
    
    

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1' , port=8000)
