from lxml import html
import requests
from collections import Counter
from matplotlib import pyplot as plt

#use requests.get to retrieve the web page with our data, parse it using the html module and save the results in tree:
page = requests.get("https://www.arrowcast.net/fids/mco/fids.asp?airline=&number=&city=&start=360&end=1410&limit=&search=Search&sort=%40actual&sortorder=asc&adi=D&hidFlightTotal=0")
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
#we only need the hours so we'll trim the rest
flights = []
for i in range(len(flight_gates)):
    if flight_gates[i] > 99:
        flights.append(int(depart_times[i][5:7]))
                
schedule = Counter(flights)

plt.plot(schedule.keys(), schedule.values(), linestyle = 'solid', marker = 'o')
plt.xlabel("Time")
plt.ylabel("Flights")
plt.title("Flight forecast")