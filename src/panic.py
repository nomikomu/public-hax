# print('hello %s!' % name)	// print('hello {0}!'.format("defm03"))
# webbrowser.open('http://...')
#
# defm03 - Kamil Żak (defm03@outlook.jp)

import urllib.request
import webbrowser
from xml.etree.ElementTree import parse
import time

office_lat = 41.980262 	
office_lon = -87.668452 
API_key = "AIzaSyDy2DZ5h77e-NxIX6Zp3UurDYK9mIqn_Pk"

close_bus_drivers_id = []


# NS -- ignore some stuff: approx
# monitor of distance
def distance(lat1, lat2):
	# returns distance in miles between two lats
	return 69*abs(lat1 - lat2)

def monitor():
	u = urllib.request.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
	# gets xml file - bus tracker
	data = u.read() # reads all from u to a data variable
	f = open('rt22.xml','wb')
	f.write(data) # writes all from data to rt22.xml file

	doc = parse('rt22.xml') 

	for bus in doc.findall('bus'):
		lat = float(bus.findtext('lat')) 
		if lat <= office_lat:
			id_of_bus = bus.findtext('id')
			direction_of_bus = bus.findtext('d')
			if direction_of_bus.startswith('North'):
				print("<alert@> We found bus: ", id_of_bus, direction_of_bus, lat)
				close_bus_drivers_id.append(id_of_bus)

				if ' ' in direction_of_bus:
					direction_of_bus.replace(' ', '+')

				lon = bus.findtext('lon')

				# Open browser with google static map API
				webbrowser.open('http://maps.googleapis.com/maps/api/staticmap?center={0},Chicago'.format(direction_of_bus)+
								'&zoom=13&size=800x800&maptype=roadmap&markers=color:red%7Clabel:S%7C{0},{1}'.format(lat, lon)+
								'&sensor=false&key={0}'.format(API_key))

				print(id_of_bus, " ", distance(office_lat,lat), " miles")
		#d = bus.findtext('d') # direction of a bus
		#print(d)
		#lat = float(bus.findtext('lat')) # to float
		#print(lat)
	
	print('-' * 8)

# running main loop
while True:
	print("bus list\n"+"========")
	monitor()
	time.sleep(60)
	# refresh rate: set to 60 seconds
