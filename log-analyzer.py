import os, csv, itertools, json

# Function to get the files of a directory
def getFiles(path):
    files = []
    for file in os.listdir(path):
        if file.endswith(".log") and not os.path.isdir(path + file):
            files.append(path + file)
    return files

# Function to get the path to the log file or the directory where the logs are stored
def getPath():
    paths = []
    control = "y"
    while (control != "n"):
        path = input("Path: ")
        if os.path.isfile(path):
            if path.endswith(".log"):
                paths.append(path)
                print("Do you want to add another file? (Y/n)")
                control = input()
            else:
                print("The path is not a log file. Do you want to add another file? (Y/n)")
                control = input()
        elif os.path.isdir(path):
            files = getFiles(path)
            if len(files) > 0:
                paths.extend(files)
                print("Do you want to add another file? (Y/n)")
                control = input()
            else:
                print("The directory does not contain any log files. Do you want to add another file? (Y/n)")
                control = input()
        else:
            print("The path is not a valid path. Do you want to add another file? (Y/n)")
            control = input()
    return paths

# Function to read a csv file field by field
def readCSV(file):
    with open(file, "r") as f:
        lines = []
        for line in f:
            line = line.rstrip()
            lines.append(line)
        return lines

# Function to get the most common value of a field in a CSV file
def getMostCommon(file, field):
    # Get the list of lines in the csv file
    lines = readCSV(file)
    # Get the list of values inside each entry of the csv
    values = []
    for line in lines:
        value = line.split()
        values.append(value)
    clientIP = []
    for value in values:
        # Get the client IP. The field value defines the field position to be used
        try:
            clientIP.append(value[field])
        # The IndexError exception is catched for entries that do not have the field
        except IndexError:
            pass
    # Get the most common value in the list
    mostCommon = max(set(clientIP), key=clientIP.count)
    # Return the most common value
    return mostCommon

# Function to get the least common value of a field in a CSV file
def getLeastCommon(file, field):
    # Get the list of lines in the csv file
    lines = readCSV(file)
    # Get the list of values inside each entry of the csv
    values = []
    for line in lines:
        value = line.split()
        values.append(value)
    clientIP = []
    for value in values:
        # Get the client IP. The field value defines the field position to be used
        try:
            clientIP.append(value[field])
        except IndexError:
            pass
    # Get the least common value in the list
    leastCommon = min(set(clientIP), key=clientIP.count)
    # Return the least common value
    return leastCommon

'''

Function to group the timestamps that are in the same second and count the events of those timestamps.
It is assumed that each timestamp is an event. The function returns the number of events in each second.

'''
def eventsPerSecond(file, field):
    lines = readCSV(file)
    values = []
    for line in lines:
        value = line.split()
        values.append(value)
    timeStamps = []
    for value in values:
        # The time stamp from the first field is obtained and stored
        try:
            timeStamps.append(value[field])
        except IndexError:
            pass
    # Iteration to go trough the timestamps and order the ones in the same second
    iterator = itertools.groupby(timeStamps, lambda string: string.split('.')[0])
    result = []
    events = []
    # The timestamps that are in the same second are stored in a new list
    for element, group in iterator:
        result.append(list(group))
    # A new list is made with the number of events in each timestamp/second
    for item in result:
        # The number of events in each second is obtained
        events.append(len(item))
    return events

# Function that adds the response header size and the response size in bytes of all the entries
def totalBytesExchanged(file, field, field1):
    # Get the list of lines in the csv file
    lines = readCSV(file)
    # Get the list of values inside each entry of the csv
    values = []
    for line in lines:
        value = line.split()
        values.append(value)
    responseSize = []
    for value in values:
        # Sum of header and response
        try:
            add = int(value[field]) + int(value[field1])
            responseSize.append(add)
        except IndexError:
            pass
    # The added value of each entry is added to the total
    listSum = sum(responseSize)
    return listSum

# Function to interact with the user and pick the preferred option
def let_user_pick(options):
    dynamicList = []
    print("Please, select an option:")
    for idx, element in enumerate(options):
        print("{}) {}".format(idx,element))
        dynamicList.append(element)
    i = input("Enter number: ")
    try:
        if 0 <= int(i) <= len(options):
            return dynamicList[int(i)]
    except:
        pass
    return None

print("Welcome to the log analyzer tool. This tool will help you analyze your logs. Please, specify the path to the log file or the directory where the logs are stored:")
pathToAnalyze = getPath()

'''

Using the following list, new options can be added extending the capabilites of the log analyzer CLI tool.

'''
options = ["Most frequent IP", "Least frequent IP", "Events per second", "Total amount of bytes exchanged", "Exit the program and do the operations"]
# A results list is used to know which operations were choosen and need to be performed
results = [0] * 4
# The values dumped to the output json are initialized to a default value
mostCommon = leastCommon = events = totalBytes = "-"

'''

The "while" loop is used to keep the program running until the user decides to exit the program. The "choosenOption" variable keeps track of the option chosen by the user.

'''
while True:
    choosenOption = let_user_pick(options)
    '''
    
    The following code will be executed depending on the option chosen by the user.
    
    '''
    if choosenOption == "Most frequent IP":
        try:
            options.remove("Most frequent IP")
        except:
            print("That option was already used. Please, select another option.")
            continue
        # The initial position of "results" is changed to 1 to indicate that the "Most frequent IP" operation needs to be done
        results[0] = 1
    elif choosenOption == "Least frequent IP":
        try:
            options.remove("Least frequent IP")
        except:
            print("That option was already used. Please, select another option.")
            continue
        results[1] = 1
    elif choosenOption == "Events per second":
        try:
            options.remove("Events per second")
        except:
            print("That option was already used. Please, select another option.")
            continue
        results[2] = 1
    elif choosenOption == "Total amount of bytes exchanged":
        try:
            options.remove("Total amount of bytes exchanged")
        except:
            print("That option was already used. Please, select another option.")
            continue
        results[3] = 1
    elif choosenOption == "Exit the program and do the operations":
        for item in pathToAnalyze:
            if results[0] == 1:
                # Int value "2" is used to refer to the field position of the client IP based on sample input file
                mostCommon = getMostCommon(item, 2)
            if results[1] == 1:
                leastCommon = getLeastCommon(item, 2)
            if results[2] == 1:
                # Int value "0" is used to refer to the field position of the timestamp based on sample input file
                events = eventsPerSecond(item, 0)
            if results[3] == 1:
                # The "totalBytesExchanged" function recieves as parameters the fields related to the response header size and the response size in bytes
                totalBytes = totalBytesExchanged(item, 1, 4)           
            # A dictionary is created and dumped to a new json file for every log file in the paths to analyze list
            dictionary = {"file": item, "most frequent IP": mostCommon, "least frequent IP": leastCommon, "total bytes exchanged": totalBytes, "events per second": events}
            with open(item+"-output.json", "w") as outfile:
                json.dump(dictionary, outfile)
            print("The ouput path for '{}' is: '{}-output.json'".format(item, item))
        break
    else:
        print("Not a valid option number.")
