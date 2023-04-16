# RouteEstimator :airplane: 

**`Created 2020`**

## Description 
This program was created in my first semester of computer science, so it may not follow coding standards completely and will have inefficiencies. 
This is a CLI-based program that calculates the travel time for five modes of transport between any two major cities on earth. 
The user is then able to graph the travel times on either a Pandas, Matplotlib or programmatically generated (using the Turtle library) chart.

There are two functions of the program:
- The route estimator lets the user input the cities manually and calculate the travel time between them.
  It also gives the option to plot a chart of the data.
- The file writer outputs travel time results to a csv file. 
  It has 10 preset origin and destination cities (go to line:297 to change origin and destination values).

![Route Estimator](https://github.com/joet-dev/RouteEstimator/blob/master/hyperlopp.PNG?raw=true)

**How it works**

The program reads all city and transport mode data from a csv. It prompts the user to enter an origin and destination city, then checks to see if the input matches a city from the city list. If there is no match, the program finds the closest matching city name to the input string (using the Levenshtein method). Once the origin and destination cities have been selected, the program calculates the distance from longitudinal and latitudinal points (using the Haversine formula), then finally calculates the time it would take for each method of transport to travel the distance. The user is then able to plot the values on a chart to compare them visually.


## TODO: 
- Create a GUI for the program to make it more user-friendly. 
- Maximise program efficiency through lookup methods. 
