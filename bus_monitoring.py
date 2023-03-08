#!/home/brugger/projects/skyss_monitor/venv/bin/python
# Stupid graphQL query editor:
# https://api.entur.io/graphql-explorer/journey-planner-v3?query=%7B%0A%20%20stopPlace%28id%3A%20%22NSR%3AStopPlace%3A548%22%29%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%20%20estimatedCalls%28timeRange%3A%2072100%2C%20numberOfDepartures%3A%2010%29%20%7B%0A%20%20%20%20%20%20realtime%0A%20%20%20%20%20%20aimedArrivalTime%0A%20%20%20%20%20%20aimedDepartureTime%0A%20%20%20%20%20%20expectedArrivalTime%0A%20%20%20%20%20%20expectedDepartureTime%0A%20%20%20%20%20%20actualArrivalTime%0A%20%20%20%20%20%20actualDepartureTime%0A%20%20%20%20%20%20date%0A%20%20%20%20%20%20forBoarding%0A%20%20%20%20%20%20forAlighting%0A%20%20%20%20%20%20destinationDisplay%20%7B%0A%20%20%20%20%20%20%20%20frontText%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20serviceJourney%20%7B%0A%20%20%20%20%20%20%20%20journeyPattern%20%7B%0A%20%20%20%20%20%20%20%20%20%20line%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20%20%20%20%20transportMode%0A%20%20%20%20%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20line%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20notices%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20publicCode%0A%20%20%20%20%20%20%20%20text%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A
# Kim Brugger (07.03.2023) kbr(at)brugger.dk

import sys
import re
import pprint as pp

import datetime

from python_graphql_client import GraphqlClient


import kbr.datetime_utils as datetime_utils


STOPID = "NSR:StopPlace:62412"

busses = {'27': 'Åsane terminal',
            '16E': 'Øyjorden',
            '12': 'Lønborglien',
            '6': 'Lyngbø',
            '5': 'Fyllingsdalen terminal'}

def main():

    # Instantiate the client with an endpoint.
    client = GraphqlClient(endpoint="https://api.entur.io/journey-planner/v3/graphql")

    # Create the query string and variables required for the request.
    query = """
            {
            stopPlace(id: \"""" + STOPID +"""\" ) {
                name
                id
                estimatedCalls(numberOfDepartures: 50, whiteListedModes: [bus]) {
                expectedDepartureTime         
                aimedDepartureTime       

                destinationDisplay {
                    frontText
                }
                serviceJourney {
                    line {
                    publicCode
                    }
                }
                notices {
                    id
                    publicCode
                    text
                }                
                }
            }
            } 
   """

    # Synchronous request
    data = client.execute(query=query)
#    pp.pprint(data)  # => {'data': {'country': {'code': 'CA', 'name': 'Canada'}}}

    data = data['data']['stopPlace']['estimatedCalls']

    used_adt = {}



    bus_blocks  = {}
    bus_times   = {}
    bus_notices = {}

    for d in data:
#        print( d['destinationDisplay'])
        if d['serviceJourney']['line']['publicCode'] in busses and d['destinationDisplay']['frontText'] in busses.values():
#            pp.pprint( d )

            # sometimes there are doublets, so this will get rid of them
            bus_nr = d['serviceJourney']['line']['publicCode']
            at_string = f"{bus_nr}/{d['aimedDepartureTime']}"

            if at_string in used_adt:
                continue

            used_adt[ at_string ] = 1

            dt = datetime_utils.string_to_datetime(d['expectedDepartureTime'])
            at = datetime_utils.string_to_datetime(d['aimedDepartureTime'])
            notices = d['notices']

            colour = 'green'

            depature_diff = (dt - at).total_seconds()

            if  depature_diff > 60*5:
                colour = 'coral'
            elif  depature_diff > 60*2:
                colour = 'orange'

            if notices != []:
                colour = 'red'

            dt =  datetime_utils.to_string(dt, "%H:%M")

            if bus_nr not in bus_times:
                bus_blocks[bus_nr] = f'<span foreground="white" background="{colour}"> {bus_nr} </span>'
                bus_times[bus_nr] = []

            bus_times[bus_nr].append( dt )
            bus_notices[ bus_nr ] = notices

#            print(f"27: {dt} {notices}")


    print("<txt>", end='')
    for bus_nr in sorted(bus_blocks.keys(), key = lambda x: int(x.replace("E", ''))):
        print( bus_blocks[bus_nr], end= '')
    
    print("</txt>", end='')

    times = []
    for bus_nr in sorted(bus_blocks.keys(), key = lambda x: int(x.replace("E", ''))):
        times.append(f"{bus_nr} - {busses[bus_nr]}: {' '.join(bus_times[bus_nr])} {bus_notices[bus_nr]}")
    print("<tool>"+"\n".join(times)+"</tool>")


if __name__ == "__main__":
    main()
