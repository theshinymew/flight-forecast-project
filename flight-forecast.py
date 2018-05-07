import sys
from lxml import html
import requests
from matplotlib import pyplot as plt
import numpy as np

#use requests.get to retrieve the web page with our data, parse it using the html module and save the results in tree
#command line arguments are used in the url so that start and end time can be specified when running the script
page = requests.get("https://www.arrowcast.net/fids/mco/fids.asp?airline=&number=&city=&start=" + sys.argv[1] + "&end=" + sys.argv[2] + "&limit=&search=Search&sort=%40actual&sortorder=asc&adi=D&hidFlightTotal=0")
tree = html.fromstring(page.content)

#use xpath function with query to retrieve the flights' time of departure and gate
depart_times = tree.xpath('//*[@id=\"tableGrid\"]/tbody/tr/td[6]/text()')
#use text_content and strip to remove unncecessary space character
depart_gates = [td.text_content().strip() for td in tree.xpath('//*[@id=\"tableGrid\"]/tbody/tr/td[9]')]

#this is the part whrere i give up and hardcode the list of elements that  I'm going to need to graph anything properly
#morning hours, 5am to 1pm, value 5 to 13
amlabels = ["5am", "6am", "7am", "8am", "9am", "10am", "11am", "12pm", "1pm"]
amhours = range(5, 14)
#afternoon hours, 1pm to 1am, values 13 to 25
pmlabels = ["1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm", "12am", "1am"]
pmhours = range(13, 26)

#make assignments corresponding to time
if sys.argv[1] == '300':
    labels = amlabels
    flights = dict.fromkeys(amhours, 0)
else:
    labels = pmlabels
    flights = dict.fromkeys(pmhours, 0)

#convert gate numbers from unicode string to int for easy use
flight_gates = []
for gate_number in depart_gates:
    gate_number = int(gate_number) if gate_number else 0
    flight_gates.append(gate_number)
    
#keep only the flight times for gates 100+, which is the terminal where i work
#we only need the date and hour so we'll trim the minutes ddd hh:mm
current_day = depart_times[0][:3]                   #store current day which should be the
                                                    #first three letters of the time at the
                                                    #begining of the list
                                            
#calculate and store the amount of flights by hour but only for gates 100+
for i in range(len(flight_gates)):
    if flight_gates[i] > 99:
        hour = int(depart_times[i][5:7])            #keep hour value of the time of flight, this will function as our key
        if current_day == depart_times[i][:3]:      #check we're still on the same day otherwise shift hour value by 11
            flights[hour] += 1
        else:
            flights[hour + 11] += 1

#Graph the results
plt.plot(flights.keys(), flights.values(), 'bo-')
plt.xlabel("Time of flight")
plt.ylabel("Number of flights")
plt.title("Flights by hour")
plt.xticks(flights.keys(), labels, rotation = 45)
#plt.show()
plt.savefig(__file__+".png", dpi = 800)
