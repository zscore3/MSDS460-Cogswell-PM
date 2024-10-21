# Critical Path Analysis 

# Adapted from the following Sources:  
## Problem description from Williams (2013, pages 95-98)
## Williams, H. Paul. 2013. Model Building in Mathematical Programming (fifth edition). New York: Wiley. [ISBN-13: 978-1-118-44333-0]

## Python PuLP solution prepared by Thomas W. Miller
## Revised April 20, 2023
## Implemented using activities dictionary with derived start_times and end_times
## rather than time decision variables as in Williams (2013)

##Printing to text file provided from GeeksforGeeks (https://www.geeksforgeeks.org/how-to-fix-permissionerror-errno-13-permission-denied-in-python/)
##daswanta_kumar_routhu (2024)

from pulp import *

# Create a dictionary of the activities and their durations
activities = {'A':2, 
              'B':2, 
              'C':2, 
              'D1':2, 
              'D2':2, 
              'D3':2, 
              'D4':2, 
              'D5':2, 
              'D6':2, 
              'D7':2, 
              'D8':2, 
              'E':2, 
              'F':2, 
              'G':2, 
              'H':2}

# Create a list of the activities
activities_list = list(activities.keys())

# Create a dictionary of the activity precedences
precedences = {'A': [], 
               'B': [], 
               'C': ['A'], 
               'D1': ['A'],  
               'D2': ['D1'], 
               'D3': ['D1'], 
               'D4': ['D2','D3'], 
               'D5': ['D4'], 
               'D6': ['D4'], 
               'D7': ['D6'], 
               'D8': ['D5','D7'], 
               'E': ['B','C'], 
               'F': ['D8','E'],
               'G': ['A', 'D8'],
               'H': ['F', 'G']}

# Create the LP problem
prob = LpProblem("Critical Path", LpMinimize)

# Create the LP variables
start_times = {activity: LpVariable(f"start_{activity}", 0, None) for activity in activities_list}
end_times = {activity: LpVariable(f"end_{activity}", 0, None) for activity in activities_list}

# Add the constraints
for activity in activities_list:
    prob += end_times[activity] == start_times[activity] + activities[activity], f"{activity}_duration"
    for predecessor in precedences[activity]:
        prob += start_times[activity] >= end_times[predecessor], f"{activity}_predecessor_{predecessor}"

# Set the objective function
prob += lpSum([end_times[activity] for activity in activities_list]), "minimize_end_times"

# Solve the LP problem
status = prob.solve()

# Print the results
print("Critical Path time:")
for activity in activities_list:
    if value(start_times[activity]) == 0:
        print(f"{activity} starts at time 0")
    if value(end_times[activity]) == max([value(end_times[activity]) for activity in activities_list]):
        print(f"{activity} ends at {value(end_times[activity])} weeks in duration")

# Print solution
print("\nSolution variable values:")
for var in prob.variables():
    if var.name != "_dummy":
        print(var.name, "=", var.varValue)

file_path = r"C:\Users\jrcog\Downloads\output.txt"

with open(file_path, "w") as file:
    file.write("Critical Path time:")
    for activity in activities_list:
        if value(start_times[activity]) == 0:
            file.write(f"\n{activity} starts at time 0")
        if value(end_times[activity]) == max([value(end_times[activity]) for activity in activities_list]):
            file.write(f"\n{activity} ends at {value(end_times[activity])} weeks in duration")
            
        # Print solution
    file.write("\nSolution variable values:\n")
    for var in prob.variables():
        if var.name != "_dummy":
            file.write(var.name)
            file.write("=")
            file.write(f"{var.varValue}")
            file.write('\n')

print("File content modified successfully!")
