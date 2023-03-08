#!/home/brugger/projects/skyss_monitor/venv/bin/python

#
# Kim Brugger (07.03.2023) kbr(at)brugger.dk

import sys
import re
import pprint as pp

import datetime

from python_graphql_client import GraphqlClient


STOPID = "NSR:StopPlace:62412"

def string_to_datetime(datetime_str: str) -> datetime:
    for time_string in time_strings:
        try:
            dt = datetime.datetime.strptime(datetime_str, time_string)
            return dt
        except Exception as e:
            #  print(e)
            pass

    raise RuntimeError(f"cannot convert datetime string '{datetime_str}' to timestamp ")

time_strings = ["%Y-%m-%dT%H:%M:%S.%f%z",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S.%fZ",  # cromwell
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S.%f%z",
                "%Y-%m-%d %H:%M:%S.%f",
                "%Y-%m-%d %H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S",
                "%a %Y-%m-%d %H:%M:%S %Z",
                "%a %Y-%m-%d %H:%M:%S",
                
                "%Y-%m-%d %Z",
                "%Y-%m-%d",
                ]



def main():

    # Instantiate the client with an endpoint.
    client = GraphqlClient(endpoint="https://api.entur.io/journey-planner/v3/graphql")

    # Create the query string and variables required for the request.
    query = """
            {
            stopPlace(id: \"""" + STOPID +"""\" ) {
                name
                id
                estimatedCalls(numberOfDepartures: 25, whiteListedModes: [bus]) {
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

    blocks = []
    details = []

    for d in data:
#        print( d['destinationDisplay'])
        if d['serviceJourney']['line']['publicCode'] == '27' and d['destinationDisplay']['frontText'] == 'Åsane terminal':
#            pp.pprint( d )
            dt = d['expectedDepartureTime']
            at = d['aimedDepartureTime']
            notices = d['notices']
            if at in used_adt:
                continue
            used_adt[ at ] = 1

            colour = 'green'

            depature_diff = (string_to_datetime(dt) - string_to_datetime(at)).total_seconds()


            if  depature_diff > 60*5:
                colour = 'coral'
            elif  depature_diff > 60*2:
                colour = 'orange'

            if notices != []:
                colour = 'red'

            dt = re.sub(r'.*T(.*):\d{2}\+.*', r'\1', dt)

            blocks.append(f'<span foreground="white" background="{colour}">27</span>')
            details.append(f'27: {dt} {notices}')


#            print(f"27: {dt} {notices}")


    print("<txt>"+"".join(blocks)+"</txt>")
    print( "<tool>"+"\n".join(details) +"</tool>")

#<txt><span foreground='white' background='green'>H</span><span foreground='white' background='grey'>Å</span><span foreground='white' background='coral'>M</span></txt>
#<tool>Haukeland sykehus: 6/13
#Årstad kirke: NA/NA
#Møllendalsplass: 2/11</tool>




if __name__ == "__main__":
    main()
