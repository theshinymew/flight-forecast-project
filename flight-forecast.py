import sys
from lxml import html
import requests
from collections import Counter
from matplotlib import pyplot as plt
from datetime import datetime

#use requests.get to retrieve the web page with our data, parse it using the html module and save the results in tree
#command line arguments are used in the url so that start and end time can be specified when running the script
page = requests.get("https://www.arrowcast.net/fids/mco/fids.asp?airline=&number=&city=&start=" + sys.argv[1] + "&end=" + sys.argv[2] + "&limit=&search=Search&sort=%40actual&sortorder=asc&adi=D&hidFlightTotal=0")
tree = html.fromstring(page.content)

#use xpath function with query to retrieve the flights' time of departure and gate
depart_times = tree.xpath('//*[@id=\"tableGrid\"]/tbody/tr/td[6]/text()')
#use text_content and strip to remove unncecessary space character
depart_gates = [td.text_content().strip() for td in tree.xpath('//*[@id=\"tableGrid\"]/tbody/tr/td[9]')]

#convert gate numbers from unicode string to int for easy use
flight_gates = []
for gate_number in depart_gates:
    gate_number = int(gate_number) if gate_number else 0
    flight_gates.append(gate_number)
    
#keep only the flight times for gates 100+, which is the terminal where i work
#we only need the date and hour so we'll trim the minutes (format is ddd hh:mm) and format as hhxm
flights = []
for i in range(len(flight_gates)):
    if flight_gates[i] > 99:
        flight_hour = datetime.strptime(depart_times[i][5:7], "%H")
        flight = flight_hour.strftime("%I%p")
        flights.append(flight)

schedule = Counter(flights)

print schedule

plt.bar(schedule.keys(),
        schedule.values(),
        1,
        align = 'edge')

plt.xlabel("Time of flight")
plt.ylabel("Number of flights")
plt.title("Flights by hour")
plt.show()