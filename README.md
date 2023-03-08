# bus_monitor

Simple monitor for showing bus times for a selection of busses from a single bus stop. Running it in a generic monitor app in xfce.

Will colour the noties depending on predicted delay times from green to coral, red means that there is a notice on the line. Often because of delays such as closed roads.

One need to find the id of the stop using this website:

```
https://stoppested.entur.org/?stopPlaceId=NSR:StopPlace:62412 
```


The script uses the API from entur.no 



And here is the link to the graphQL editor as the documentation is a bit lacking...
```
https://api.entur.io/graphql-explorer/journey-planner-v3?query=%7B%0A%20%20stopPlace%28id%3A%20%22NSR%3AStopPlace%3A548%22%29%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%20%20estimatedCalls%28timeRange%3A%2072100%2C%20numberOfDepartures%3A%2010%29%20%7B%0A%20%20%20%20%20%20realtime%0A%20%20%20%20%20%20aimedArrivalTime%0A%20%20%20%20%20%20aimedDepartureTime%0A%20%20%20%20%20%20expectedArrivalTime%0A%20%20%20%20%20%20expectedDepartureTime%0A%20%20%20%20%20%20actualArrivalTime%0A%20%20%20%20%20%20actualDepartureTime%0A%20%20%20%20%20%20date%0A%20%20%20%20%20%20forBoarding%0A%20%20%20%20%20%20forAlighting%0A%20%20%20%20%20%20destinationDisplay%20%7B%0A%20%20%20%20%20%20%20%20frontText%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20serviceJourney%20%7B%0A%20%20%20%20%20%20%20%20journeyPattern%20%7B%0A%20%20%20%20%20%20%20%20%20%20line%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20%20%20%20%20transportMode%0A%20%20%20%20%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20line%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20notices%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20publicCode%0A%20%20%20%20%20%20%20%20text%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A
```
