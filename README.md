# JSON_Visualizer
   
   A versatile Python-based (Python 3.10) web application designed for viewing Dataset-JSON files. This tool is compatible with files adhering to the JSON 1.1 schema and supports both JSON and NDJSON formats. This guide will help you get started and maximize your use of this tool.

# Authors:
  1.	Deepika Senthilkumar
  2.	Sai Pooja V R
  3.	Swetha Rameswaran

# Getting Started
Follow these steps to set up and run the tool on your local machine.

### Clone the repository
1. Open Git Bash
2. Change the current working directory to the location where you want the cloned directory.
3. Type git clone, and then paste the URL you copied earlier.
   
  ```
  git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY  
  ```

4. Enter to create your local clone.

### Package Installation

  ```
  pip install -r /path/to/requirements.txt
  ```
----

### To run the application, run this command after cloning.

```
python app.py
```
### Overview:

1. Compatible with both edge and chrome extensions
2. Recommended default screen size is 75-80%.
3. Home page enables the user to upload the JSON & NDJSON files
    o	By clicking ‘View’ button, the user is directed to second page which has three tabs ‘RAW JSON’, ‘METADATA’ and ‘DATA’.
    o	RAW JSON tab displays the JSON in dictionary format
    o	METADATA and DATA tabs has the respective data and metadata in table format.
 4. The METADATA and DATA tabs feature filtering and sorting functionalities, allowing users to sort or filter based on various conditions.
 5. Additionally, there is a search bar to quickly find specific words within the table.
 6. The Burger menu on the right enables the user to go back to the HOME page

Note: This is a submission to CDISC Hackathon 2024 From team SDSA, Pfizer.
