__author__ = "Joseph Thurlow"
__version__ = "0.4.0"
__email__ = "JCT020@student.usc.edu.au"

"""
This program calculates the travel time for 5 modes of transport between any two major* cities on earth. 
There are two functions of the program:
- The route estimator lets the user input the cities manually and calculate the travel time between them.
  It also gives the option to plot a chart of the data.
- The file writer outputs travel time results to a csv file. 
  It has 10 preset origin and destination cities (go to line:297 to change values).
"""

from math import radians, cos, sin, asin, sqrt, e
import numpy as np
import pandas as pd
import sys
import os
import csv
import turtle
import matplotlib.pyplot as plt
import matplotlib.pyplot as plot


class Program:
    def __str__(self):
        """
        This function returns information about the file and it's author
        :return: Returns the author, program version, and e-mail.
        """
        return 'Author: Joseph Thurlow\nVersion: 0.4.0\nE-mail: JCT020@student.usc.edu.au'

    def __init__(self):
        """
        __init__ reads the relevant files and creates lists from the spread sheets.
        Initialises the class attributes.
        """
        # Reads the sheets within th excel file (.xlsx)
        # !NOTE!: The REA.xlsx file must be in the same directory as the program!!!
        os.chdir(sys.path[0])  # Get the program directory and set it as the working directory.
        rea_file = pd.ExcelFile('REA.xlsx')
        df_geo_city = pd.read_excel(rea_file, 'geo_city')
        df_transport = pd.read_excel(rea_file, 'speed')

        # Initialises class variables.
        self.city_list = df_geo_city.values.tolist()
        self.modes_list, self.speeds_list = zip(*df_transport.values.tolist())
        self.start_end = ""  # Contains the string for either the "destination" or "origin.
        self.input = ""  # Stores both the origin and destination city input by the user.
        self.turtle_bar_chart = 1  # Used to make sure that the turtle bar chart doesnt run more than once.
        # Contains data for the selected origin city. Format: City, Country, Latitude, Longitude.
        self.ocity_list = []
        # Contains data for the selected destination city. Format: City, Country, Latitude, Longitude.
        self.dcity_list = []
        # Contains travel time data for each mode of transport. Format: [[hours, minutes], ...
        # The list of travel times are ordered such that the values correspond to transports_list order.
        self.times_list = []

    def restart(self):
        """
        Allows the user chooses whether to close the program or restart it.
        """
        confirm = input("\nPress any key to restart. Press X to exit. ")
        print("\n")
        if confirm.lower().strip() == 'x':
            self.re_exit()
        else:
            self.start()

    def re_exit(self):
        """
        Prints exit message. Terminates the program.
        """
        print('{:-^46}'.format("Program Terminated"))
        sys.exit()

    def city_input(self, start_end):
        """
        Receives an input and checks whether the user has input 'na'. If not, it returns a city_check() of the data.
        :param start_end: String used that decides whether the user needs to input the origin or destination city.
        :return: city_check() of the input.
        """
        self.start_end = start_end
        self.input = input("Input " + self.start_end + " city: ")
        if self.input.lower().strip() == "na":
            self.re_exit()
        return self.city_check()

    def city_check(self):
        """
        Checks the database for the input to find the city information. If the city is not in the database it runs the
        spell check function. If the spell check finds the correct city, city_check() is called again with the new value.
        :return: The list of data for the city containing the City, Country, latitude, and longitude (in that order).
        """
        # Loops through the whole list of cities to find an exact match with the input.
        for city_idx in range(len(self.city_list)):
            self.input = self.input.strip()
            if self.city_list[city_idx][1].lower() == self.input.lower():
                city_country = self.city_list[city_idx][0]
                city_name = self.city_list[city_idx][1]
                city_latitude = self.city_list[city_idx][2]
                city_longitude = self.city_list[city_idx][3]
                city_info_list = [city_name, city_country, city_latitude, city_longitude]
                return city_info_list

        # Lets the user know their input was not found.
        # Runs spell check then calls the function with the new input string.
        print("No entry for " + self.input + " in database.")
        self.input = self.spell_check()
        return self.city_check()

    def spell_check(self):
        """
        Finds the closest match to the city input. The city with the lowest difference from the input string is
        suggested to the user. If the user refuses the suggested city value, the program calls to the restart function.
        If the assumed city is correct the program returns the assumed city.
        :return: The closest city to the original city input.
        """
        print('{:-^46}'.format("Searching for alternative"))
        city_names = [self.city_list[i][1] for i in range(len(self.city_list))]  # List of city names.

        # Creates the list of Levenshtein distance values using the Levenshtein method.
        # The Levenstein distance is a measurement of the difference between two strings.
        index_diff = []
        for idx in range(len(city_names)):
            matrix_x = len(self.input) + 1
            matrix_y = len(city_names[idx]) + 1
            matrix = np.zeros((matrix_x, matrix_y))
            for x in range(matrix_x):
                matrix[x, 0] = x
            for y in range(matrix_y):
                matrix[0, y] = y

            for x in range(1, matrix_x):
                for y in range(1, matrix_y):
                    if self.input[x - 1] == city_names[idx][y - 1]:
                        matrix[x, y] = min(
                            matrix[x - 1, y] + 1,
                            matrix[x - 1, y - 1],
                            matrix[x, y - 1] + 1)
                    else:
                        matrix[x, y] = min(
                            matrix[x - 1, y] + 1,
                            matrix[x - 1, y - 1] + 1,
                            matrix[x, y - 1] + 1)
            index_diff.append(matrix[matrix_x - 1, matrix_y - 1])

        assumed_city_index = index_diff.index(min(index_diff))  # The index of the city with the lowest 'difference'
        # Checks if the assumed city is correct.
        while True:
            cond_correction = input("Did you mean to input " + city_names[assumed_city_index] + "? (Y/N) ")
            if cond_correction.lower().strip() == 'y':
                print("Your " + self.start_end + " location has been set to " + city_names[assumed_city_index] + ".\n")
                return city_names[assumed_city_index]
            elif cond_correction.lower().strip() == 'n':
                print("Unable to locate city in database.")
                self.restart()
            else:
                print('{:-^46}'.format("***Invalid Input***"))
                continue

    def latlng_to_dist(self):
        """
        Calculates the distance between two latitude and longitude points using Haversine formula.
        :return: The distance between two points in kilometers rounded to 2 decimal places
        """
        origin_lat, origin_lng, dest_lat, dest_lng = self.ocity_list[2], self.ocity_list[3], self.dcity_list[2], self.dcity_list[3]
        radius_of_earth = 6371
        int_lat1 = radians(origin_lat)
        int_lat2 = radians(dest_lat)
        lat_diff = int_lat1 - int_lat2
        lng_diff = radians(origin_lng - dest_lng)
        a = sin(lat_diff / 2.0) ** 2 + cos(int_lat1) * cos(int_lat2) * sin(lng_diff / 2.0) ** 2
        distance = 2 * radius_of_earth * asin(sqrt(a))
        return round(distance, 2)

    def travel_time(self, distance):
        """
        Calculates the travel time for 5 modes of transport with the distance given.
        :param distance: The distance in kilometers.
        :return: The list of times for each mode of transport
        """
        print("The travel time between " + self.ocity_list[0] + " and " + self.dcity_list[0] + " is:")
        self.times_list = []  # Erases all past data from the list.
        # The code below calculates the travel time using distance/speed.
        # It also adjusts the travel time to account for wait times and refuelling.
        # The algorithms to calculate the travel time adjustment are reverse-engineered from hyperloop-one.com
        for row in range(len(self.modes_list)):
            time_min = float(distance) / (float(self.speeds_list[row]) / 60)
            if row == 0:
                # Calculation for hyperloop.
                time_min *= ((5.84 * (1 / (1.26 * time_min - 1.02))) + 1.2017)
            elif row == 1:
                # Calculation for airplane. Adds 2 hours if the flight is domestic.
                # Adds 3 hours if the flight is international.
                if self.ocity_list[1] == self.dcity_list[1]:
                    time_min += 120
                else:
                    time_min += 180
            elif row == 2 or row == 3:
                # Calculation for both HSP and rail.
                time_min *= ((30 * (1 / (0.9888 * time_min - 1.402))) + 1.2987)
            else:
                # Calculation for car.
                time_min *= 1.35
            time_hour = int(time_min) // 60
            time_min = int(time_min) % 60
            print("It takes: " + (str(time_hour) + "h." + str(round(time_min, 0)) + "m.").ljust(8) + " by " +
                  self.modes_list[row])
            self.times_list.append([int(time_hour), int(round(time_min, 0))])

    def bar_charts(self):
        """
        User interface for Bar Charts. Allows the user to select a chart.
        Removes the turtle chart from the list of options and doesn't allow the user to select the turtle chart if
        the chart has already been opened previously in the program.
        """
        while True:
            print("\n{:-^46}".format("Bar Charts"),
                  "\nt - Turtle ~ Horizontal Bar Chart" * self.turtle_bar_chart,
                  "\nm - Matplotlib ~ Horizontal Bar Chart",
                  "\np - Pandas ~ Horizontal Bar Chart",
                  "\nn - No selection",
                  "\n{:-^46}".format(''))

            confirm = input("Input: ")
            if confirm.lower().strip() == 't' and self.turtle_bar_chart == 1:
                self.turtle_bar_chart = self.turtle_hbc()
            elif confirm.lower().strip() == 'm':
                self.mpl_hbc()
            elif confirm.lower().strip() == 'p':
                self.pd_hbc()
            elif confirm.lower().strip() == 'n':
                break
            else:
                print('{:-^46}'.format("*** Input Error ***"))
                continue
            while True:
                confirm = input("\nOpen another chart? (Y/N) ")
                if confirm.lower().strip() == 'y':
                    self.bar_charts()
                elif confirm.lower().strip() == 'n':
                    break
                else:
                    print('{:-^46}'.format("*** Input Error ***"))
                    continue
            break
        self.restart()

    def change_input(self):
        """
        User interface for changing the origin or destination city. Also has an exit option.
        """
        while True:
            print('\n{:-^46}\n'.format("Task Selection") +
                  "o - Change the origin city\n"
                  "d - Change the destination city\n"
                  "x - Exit\n"
                  '{:-^46}\n'.format(""))
            confirm = input("Input task: ")
            if confirm.lower().strip() == 'd':
                self.dcity_list = self.city_input('new destination')
                break
            elif confirm.lower().strip() == 'o':
                self.ocity_list = self.city_input('new origin')
                break
            elif confirm.lower().strip() == 'x':
                self.re_exit()
            else:
                print('{:-^46}'.format("*** Input Error ***"))
                continue

    def main_program(self):
        """
        Main user interface for the "Route Estimator" task.
        The user enters origin and destination city. Then the travel times between the cities are output.
        It also gives the option to opening a chart window displaying the data.
        """
        print('{:-^46}'.format("Route Estimator"))
        print("Enter any city name. Enter NA to exit program.")
        self.ocity_list = self.city_input('origin')
        self.dcity_list = self.city_input('destination')
        while True:
            confirm = input("Confirm to find the travel time between {}, {} and {}, {}. (Y/N) "
                            .format(self.ocity_list[0], self.ocity_list[1], self.dcity_list[0], self.dcity_list[1]))
            if confirm.lower().strip() == 'y':
                distance = self.latlng_to_dist()
                self.travel_time(distance)
                self.bar_charts()
            elif confirm.lower().strip() == 'n':
                self.change_input()
            else:
                print('{:-^46}'.format("*** Input Error ***"))
                continue

    def write_to_file(self):
        """
        Creates and writes to a file. Writes the travel times for 10 different combinations of cities.
        """
        test_cities = [['Tokyo', 'Damascus'], ['Beijing', 'Moscow'], ['Cairo', 'Bangkok'], ['Mexico City', 'New York'],
                       ['Seoul', 'Istanbul'], ['Paris', 'Berlin'], ['London', 'Guangzhou'], ['Hong Kong', 'Chicago'],
                       ['Sydney', 'Melbourne'], ['Athens', 'Darwin']]

        # Create the file.
        file_path = input("Input target directory: ")
        file_path = file_path.replace("\\", "/").strip(" ")  # Replaces any backslashes for forward slashes.
        if not os.path.exists(file_path):  # Checks to make sure directory is available.
            print("Invalid directory!")
            return

        entries = os.listdir(file_path)
        file_name = 'RE_Calculations.csv'
        if file_name not in entries:  # Checks to make sure the file is not already in the directory.
            file = open(os.path.join(file_path, file_name), "w")
            rec_write = csv.writer(file, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        else:
            condition = input("\nFile is already exists in this directory.\n"
                              "Press any key to restart. Press Y to overwrite. ")
            if condition.lower().strip() == "y":
                try:
                    file = open(file_path + "/" + file_name, "w")
                    rec_write = csv.writer(file, delimiter=',', quotechar='"', lineterminator='\n',
                                           quoting=csv.QUOTE_MINIMAL)
                except IOError:  # Only runs if there is a problem opening the file.
                    print("Could not open file! Please close Excel!")
            else:
                return

        # Write to file.
        rec_write.writerow(["Origin to Destination", "Recommended travel", "Via Hyperloop", "Via Airplane",
                            "Via High-speed Rail", "Via Rail", "Via Car"])
        for origin_destination in test_cities:
            # Data retrieving
            city_list = []
            for instance in origin_destination:
                self.input = instance
                city_list.append(self.city_check())
            self.ocity_list, self.dcity_list = city_list

            # Calculations.
            distance = self.latlng_to_dist()
            self.travel_time(distance)

            # Converts hours and minutes to minutes.
            travel_times = [self.times_list[x][0] * 60 + self.times_list[x][1] for x in range(len(self.times_list))]
            # Finds the index of the fastest mode of transport.
            index_fastest = travel_times.index(min(travel_times))

            # Writes row to file.
            rec_write.writerow([self.ocity_list[0] + " to " + self.dcity_list[0],
                                self.modes_list[index_fastest],
                                "{}h.{}m.".format(*self.times_list[0]),
                                "{}h.{}m.".format(*self.times_list[1]),
                                "{}h.{}m.".format(*self.times_list[2]),
                                "{}h.{}m.".format(*self.times_list[3]),
                                "{}h.{}m.".format(*self.times_list[4])])
        file.close()

    def turtle_hbc(self):
        """
        Draws a horizontal bar chart using the turtle library.
        The bar chart contains the recommended mode of transport, title, modes of transportation, and travel time.
        """
        print('\n{:-^46}'.format('Turtle Horizontal Bar Chart'))
        print("NOTE!: The Turtle Window can only be opened once due to certain limitations. "
              "\nExit the program and restart to draw another turtle chart.")
        # Setup for the window and turtle
        t = turtle.Turtle()
        wn = turtle.Screen()
        wn.resetscreen()
        t.ht()
        wn.setup(width=800, height=600)
        wn.title("Travel Times - Turtle Horizontal Bar Chart")
        wn.bgcolor("#222")
        t.speed(0)
        t.pensize(2)

        # Setup for icons.
        # Sets the working directory.
        # NOTE: Images folder must be in the same folder as the program and contain the .gif files!
        os.chdir(os.getcwd() + "/Images")
        gif_list = ["Hyperloop.gif", "Plane.gif", "Hsr.gif", "Rail.gif", "Car.gif"]  # List of .gif file names.
        icons = True  # Lets the program know whether to run icon-printing code later on.
        for gif in gif_list:
            if gif not in os.listdir():
                # Prints an error and sets icons to false so the program doesn't try to stamp non-existent gif files.
                print("Error " + gif + " file is missing!")
                icons = False
            else:
                # Registers gif to turtlescreen's shape list to be used with shape() stamp() later on.
                wn.register_shape(gif)

        # Draws the header box
        t.pu()
        t.setposition(-400, 300)
        t.color("#00d6ab")
        t.begin_fill()
        rect_coord = [[400, 300], [400, 225], [-400, 225]]
        for coord in rect_coord:
            t.setposition(coord[0], coord[1])
        t.end_fill()

        # Draws the text in the header box
        t.color("#222")
        t.setposition(-370, 240)
        t.write("Travel time: " + self.ocity_list[0] + " - " + self.dcity_list[0], font=("Calibri", 24, "bold"))

        # Reads the data and creates relevant variables.
        travel_times_min, sorted_times_list,  sorted_tt_decimal, sorted_mode, index = self.organize_data()
        sorted_mode.reverse()
        index.reverse()
        max_tt = max(travel_times_min)  # This variable stores the maximum travel time.
        # The list below stores the minutes from least to greatest, also taking note of each values original index.
        # e.g. [(2, 60), ...] reads as 60 minutes originally stored in index 2.
        t.setposition(-200, -280)
        t.color("#c900d4")
        t.write("Recommended mode of transport: " + sorted_mode[0],
                font=("Calibri", 16, "bold"))

        # Variables used to scale the chart to the appropriate size for the window.
        scale = 600 / max_tt  # Used to make the longest travel time always 600 long (other tt are scaled accordingly).
        position_diff = 95  # Used to set the gap between bars.

        # Used to draw chart grid-lines.
        t.color("#004235")
        t.pensize(3)
        num_grid_lines = max_tt // 60
        multiplier = 1
        if num_grid_lines > 20:
            num_grid_lines = round(num_grid_lines, -1) / 10
            multiplier = 10

        for num_gridline in range(int(num_grid_lines) + 1):  # Determines the number of grid lines drawn.
            # This code basically scales the length between the grid-lines.
            t.setposition(-310 + ((60 * multiplier * scale) * num_gridline), 180)
            t.pd()
            t.setposition(-310 + ((60 * multiplier * scale) * num_gridline), -240)
            t.pu()

        # Draws the bars for each mode of transport.
        t.pensize(6)
        bar_colors = ["#c900d4", "#00d6ab", "#00d6ab", "#00d6ab", "#00d6ab"]
        for ind in range(len(travel_times_min)):
            # Extracts the original index and value into separate variables.
            t.pu()
            t.setposition(-310, 160 - position_diff * ind)  # Positioning for the beginning of the bar.
            t.pd()
            t.color(bar_colors[ind])
            t.forward(travel_times_min[ind] * scale)
            t.pu()
            turtle_x = t.xcor()
            turtle_y = t.ycor()
            t.color("#f5f5f5")
            t.setposition(turtle_x + 20, turtle_y - 8)  # Positioning to print the travel time.
            # This condition is used to print only the minutes if there are 0 hours. Avoids 0hr 10min.
            if self.times_list[index[ind]][0] == 0:
                t.write(str(self.times_list[index[ind]][1]) + "m.",
                        font=("Calibri", 12, "normal"))
            else:
                t.write(str(self.times_list[index[ind]][0]) + "hr " + str(self.times_list[index[ind]][1]) + "m",
                        font=("Calibri", 12, "normal"))

            t.setposition(-300, 130 - position_diff * ind)  # Positioning to print the mode of transport.
            t.write(sorted_mode[ind], font=("Calibri", 12, "normal"))
            if icons:  # Only runs if the icons are in the found and available.
                t.setposition(-345, 160 - position_diff * ind)  # Positioning to stamp the mode of transport icon.
                t.shape(gif_list[index[ind]])
                t.stamp()

        wn.exitonclick()
        return 0

    def mpl_hbc(self):
        """
        Uses the Matplot library to create a Horizontal Bar Chart.
        The bar chart contains the recommended mode of transport, title, modes of transportation, and travel time.
        """
        print('\n{:-^46}'.format('MatPlotLib Horizontal Bar Chart'))
        bar_colors = ["#c900d4", "#00d6ab", "#00d6ab", "#00d6ab", "#00d6ab"]
        # Retrieves and sorts the data.
        travel_times_min, sorted_times_list, sorted_tt_decimal, sorted_mode, index = self.organize_data()
        sorted_mode.reverse()  # The data needs to be adjusted because each library reads the data differently

        plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
        fig = plt.gcf()
        fig.canvas.set_window_title('Travel Times - MPL Horizontal Bar Chart')
        plt.barh(index, sorted_tt_decimal, align='center', alpha=0.5, color=bar_colors)
        plt.yticks(index, sorted_mode)
        plt.xlabel('Travel Time - Hours', fontsize=12, y=-1.02)
        plt.title('Travel Time: ' + self.ocity_list[0] + " - " + self.dcity_list[0],
                  fontsize=20, fontweight="bold", y=1.05)

        # Prints the travel times for each mode with format hr. min.
        for i in range(len(sorted_times_list)):
            plt.text(sorted_tt_decimal[-i-1], i,
                     str("   " + str(sorted_times_list[i][0]) + "hr. " + str(sorted_times_list[i][1]) + "min."),
                     va='center', color="#222222", fontweight="bold")

        plt.figtext(0.32, 0.02,
                    "Recommended mode of transport: " + sorted_mode[0],
                    fontsize=14, color="#c900d4", fontweight='bold')
        plt.show()

    def pd_hbc(self):
        """
        Horizontal Bar Chart drawn with pandas.
        The bar chart contains the recommended mode of transport, title, modes of transportation, and travel time.
        """
        print('\n{:-^46}'.format('Pandas Horizontal Bar Chart'))
        # Retrieves and sorts the data
        travel_times_min, sorted_times_list, sorted_tt_decimal, sorted_mode, index = self.organize_data()
        sorted_tt_decimal.reverse()  # The data needs to be adjusted because each library reads the data differently

        # formatting the data for plotting
        travel_time_df = pd.DataFrame({"Travel Times": sorted_tt_decimal}, index=sorted_mode)
        travel_time_df.plot.barh(figsize=(12, 8), color="#00d6ab")
        fig = plt.gcf()
        fig.canvas.set_window_title('Travel Times - Pandas Horizontal Bar Chart')
        plt.title("Travel Time: " + self.ocity_list[0] + " - " + self.dcity_list[0],
                  fontsize=16, fontweight="bold", y=1.05)
        plt.xlabel("Travel Time - Hours", fontsize=12)
        for i in range(len(sorted_times_list)):
            plt.text(sorted_tt_decimal[i], i,
                     str("   " + str(sorted_times_list[i][0]) + "hr. " + str(sorted_times_list[i][1]) + "min."),
                     va='center', color="#222222", fontweight="bold")
        plt.figtext(0.32, 0.02,
                    "Recommended mode of transport: " + sorted_mode[4],
                    fontsize=12, color="#c900d4", fontweight="bold")
        plot.show(block=True)

    def organize_data(self):
        """
        Gathers and sorts variables for use in the turtle_hbc, mpl_hbc, and pd_hbc functions.

        :return: A list containing:
                 -  travel_times_min: sorted list of travel times in minutes format.
                 -  sorted_times_list: sorted list of travel times in [[hour, min], [hour, min], ...] format.
                 -  sorted_tt_decimal: sorted list of travel times in decimal hours.
                 -  sorted_mode: sorted modes of transport. NOTE: Sorted the same way the travel times were sorted.
                 -  index
        """
        # Converts travel times to minutes.
        travel_times_min = sorted([time[0] * 60 + time[1] for time in self.times_list])
        # Converts minutes to the travel time as a float.
        travel_time_decimal = [time / 60 for time in travel_times_min]
        # Sorts the travel times from least to greatest whist noting the original index of the variable.
        sorted_tt_decimal = sorted(enumerate(travel_time_decimal), key=lambda i: i[1])
        # Splitting the original index of the time and the time into two tuples
        index, sorted_tt_decimal = zip(*sorted_tt_decimal)
        index = sorted(index, reverse=True)
        # Converting tuple sorted_tt_decimal to list
        sorted_tt_decimal = [float(x) for x in sorted_tt_decimal]
        # Converting tuple index to list
        index = [int(x) for x in index]
        # Sorts the transport modes according to the way the travel times were sorted
        sorted_mode = [self.modes_list[i] for i in index]
        sorted_times_list = [self.times_list[i] for i in index]
        return [travel_times_min, sorted_times_list, sorted_tt_decimal, sorted_mode, index]

    def start(self):
        """
        The main selection for the program. Gives the user the option decide whether to run the manual route estimator
        or create a file containing travel times for 10 cities.
        """
        while True:
            print("\n{:-^46}".format('Program Selection'),
                  "\n1 - Route Estimator",
                  "\n2 - Write calculations to file",
                  "\nx - Exit",
                  "\n{:-^46}".format(''))
            confirm = input("Select task: ")
            if confirm.strip() == '1':
                print("\n")
                self.main_program()
                self.restart()
            elif confirm.strip() == '2':
                print("\n")
                self.write_to_file()
                self.restart()
            elif confirm.lower().strip() == 'x':
                self.re_exit()
            else:
                print('{:-^46}'.format("*** Input Error ***"))
                continue


obj_program = Program()
obj_program.start()
