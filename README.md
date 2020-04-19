# memstats
Linux metric collection, graphing and publishing tool. 

The config.py file points the scripts to the correct server for installing the collection service or for reading the logs and parsing them.  The collection can happen on multiple servers as the value is a list of hostnames.   The install happens on 1 server at a time. The variable "hostname" is used by the setup script.  The list variable graphhost is used by the collection and graphing scripts.  A simple list of hostnames is all that is needed.  

There are three versions of this graphing framework.   A matplotlib, mpld3, and plotly.   There is a "runit.bat" file that shows the execution of the different scripts in order.   All log files are accessed via SSH, parsed and then normalized CSV files are created.  From there the graphig scripts can read each CSV file and generate the graphs.  There is a DEFAULT.html file that reads in a list of published graphs and allows the user to select a graph from a dropdown list.   The last line in the runit.bat is what pushes the generated files and syncs the python generation dir with the web site publish dir.  

There are example generated files in the attached directory.  
