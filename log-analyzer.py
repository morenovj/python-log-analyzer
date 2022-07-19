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
        clientIP.append(value[field])
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
        clientIP.append(value[field])
    # Get the least common value in the list
    leastCommon = min(set(clientIP), key=clientIP.count)
    # Return the least common value
    return leastCommon

# Function to group the time stamps that are in the same second and count the events of those time stamps
def eventsPerSecond(file, field):
    lines = readCSV(file)
    values = []
    for line in lines:
        value = line.split()
        values.append(value)
    timeStamps = []
    for value in values:
        # The time stamp from the first field is obtained and stored
        timeStamps.append(value[field])
    # Iteration to go trough the timestamps and order the ones in the same second
    iterator = itertools.groupby(timeStamps, lambda string: string.split('.')[0])
    result = []
    for element, group in iterator:
        result.append(len(list(group)))
        result.append(list(group))
    return result

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
            #return int(i)
    except:
        pass
    return None

print("Welcome to the log analyzer tool. This tool will help you analyze your logs. Please, specify the path to the log file or the directory where the logs are stored:")
pathToAnalyze = getPath()

'''

Using the following list, new options can be added extending the capabilites of the log analyzer CLI tool.

'''
options = ["Most frequent IP", "Least frequent IP", "Events per second", "Total amount of bytes exchanged", "Exit the program"]
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
        for item in pathToAnalyze:
            #print("The most frequent IP is: {}".format(getMostCommon(item)))
            # Int value "2" is used to refer to the field position of the client IP based on sample input file.
            dictionary = {"file": item, "most frequent IP": getMostCommon(item, 2)}
            with open(item+"-output.json", "a") as outfile:
                json.dump(dictionary, outfile)
    elif choosenOption == "Least frequent IP":
        try:
            options.remove("Least frequent IP")
        except:
            print("That option was already used. Please, select another option.")
            continue
        for item in pathToAnalyze:
            #print("The least frequent IP is: {}".format(getLeastCommon(item)))
            # Int value "2" is used to refer to the field position of the client IP based on sample input file.
            dictionary = {"file": item, "least frequent IP": getLeastCommon(item, 2)}
            with open(item+"-output.json", "a") as outfile:
                json.dump(dictionary, outfile)
    elif choosenOption == "Events per second":
        try:
            options.remove("Events per second")
        except:
            print("That option was already used. Please, select another option.")
            continue
        for item in pathToAnalyze:
            # Int value "0" is used to refer to the field position of the timestamp based on sample input file.
            print(eventsPerSecond(item, 0))
    elif choosenOption == "Total amount of bytes exchanged":
        try:
            options.remove("Total amount of bytes exchanged")
        except:
            print("That option was already used. Please, select another option.")
            continue
    elif choosenOption == "Exit the program":
        break
    else:
        print("Not a valid option number.")
