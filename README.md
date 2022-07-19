# Python Log Analyzer CLI

Python Log Analyzer CLI is a tool that takes as an **input** the path to a log file or directory containing logs. With those inputs, the user can choose among a list of options
to perform operations on the given input logs. The **output** will be the path to a JSON format file that contains the result of those operations. Each input file will have it's own output file.

## Getting Started
### Requirements
**No** external packages are needed:
* Python >= 3.7
* An input log file. The script is adapted to work with the fields from the following [sample set] (*Data from SecRepo website https://www.secrepo.com/#about published under a Creative Commons Attribution 4.0 International License*). Please, refer to the *About The Code* section in order to learn how to adapt the script for different
input files.
* Docker engine in case of using the script with the Dockerfile method. Refer to the [official docker documentation].

### Usage
Run the script with the following command:

```bash
python3 log-analyzer.py
```

**OR**
 
Build an image using the *Dockerfile*:

```bash
docker build -t python-log-analyzer-image .
```

Then run the recently created image:

```bash
docker run -it python-log-analyzer-image
```


## Example

1. Script is initialized and a path to a log file is being passed as an input. The script also accepts a path to a
directory searching for any .log file available:
```sh
$ python3 log-analyzer.py 
Welcome to the log analyzer tool. This tool will help you analyze your logs. Please, specify the path to the log file or the directory where the logs are stored:
Path: /path/to/directory/with/logs/sample.log
```

2. New paths can be added if required. A menu with the options available appears:

```sh
$ Do you want to add another file? (Y/n)
n
Please, select an option:
0) Most frequent IP
1) Least frequent IP
2) Events per second
3) Total amount of bytes exchanged
4) Exit the program
Enter number: 0
```
3. We can choose another option. The previously selected option disappears:

```sh
$ Please, select an option:
0) Least frequent IP
1) Events per second
2) Total amount of bytes exchanged
3) Exit the program
Enter number:
```

4. The option to exit the program is selected. The output path is printed:

```sh
$ Please, select an option:
0) Least frequent IP
1) Events per second
2) Total amount of bytes exchanged
3) Exit the program
Enter number: 3
The output path for the file "/path/to/directory/with/logs/sample.log" is "/path/to/directory/with/logs/sample.log-output.json"
```

## About the code

### Add new options to the CLI

The flexibility of the script allows the developer to add new options easily:

```python
options = ["Most frequent IP", "Least frequent IP", "Events per second", "Total amount of bytes exchanged", "Exit the program"]
```

### How to adapt the code to work with other input log formats

For different types of input files where the CSV field order is different, the main methods accept the field position
as a parameter. Therefore the code is flexible to accept input files with a different structure than the one
provided in the sample:

```python
# Function to get the most common value of a field in a CSV file
def getMostCommon(file, field):
    .....
    clientIP = []
    for value in values:
        # Get the client IP. The field value defines the field position to be used
        clientIP.append(value[field])
    .....
```

```python
if choosenOption == "Most frequent IP":
    .....
            # Int value "2" is used to refer to the field position of the client IP based on sample input file.
            dictionary = {"file": item, "most frequent IP": getMostCommon(item, 2)}
    .....
```

## Contact

[![LinkedIn][linkedin-shield]][linkedin-url]

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/jorge-moreno-velez/
[sample set]: https://www.secrepo.com/squid/access.log.gz
[official docker documentation]:https://docs.docker.com/engine/
