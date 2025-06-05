# Extract Financial Data from Financial Statement

## How to use
* Ensure python is installed
* Install dependencies by run `pip3 install -r requirements.txt`
* Ensure the source document is saved as OpenOffice xml format
* In the program directory, execute the script by run `python3 main.py path_of_the_source.xml`, where the path_of_the_source.xml is the path of the source xml file
* The result will be displayed on terminal

## Design approach
* First, scan the document XML file to identify all non-empty content blocks
* The section_detector directory in src directory contains different detectors for different designated section
* financial_report_analyzer.py loads the detectors and manage the result at the end

## Limitation
* The extraction is highly depends on the keywords in keyword.json. It only matched via regex.
