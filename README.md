# Python Project for Processing Survey Data and Interacting with Monday.com

This project is a POC (Proof-Of-Concept) Python application designed to read survey data from CSV files, process it, and create corresponding items in a Monday.com CRM board using the Monday.com GraphQL API. It also logs activities and errors, making it suitable for debugging and monitoring the data processing workflow.

## Features

- Reads survey data from CSV files.
- Processes survey records to determine priority based on survey scores.
- Creates items in Monday.com based on processed data.
- Logs all steps of the process, including file reading and API responses.

## Installation

To get started with this project, clone the repository to your local machine:

```bash
git clone https://github.com/bileshg/SurveyLoadMonday.git
cd yourprojectname
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Configuration
Before running the application, you must set up the necessary configuration:

1. Config File: Ensure the `config.ini` file in the root directory contains the correct environment settings and paths.
2. Environment Variables: The application uses environment variables stored in a .env file for API keys and sensitive data. Make sure this file exists and is populated with the correct information:

    ```
    # .env file
    MDC_API_KEY=your_monday_com_api_key_here
    ```

3. Mapping: Following is the sample data that was used for mapping the survey data to Monday.com fields. This mapping is hardcoded in the code and can be updated as needed.

    ```CSV
    Name,Email,Phone Number,Company,Survey Score,Title,Comments
   John Doe,johndoe@example.com,555-0100,Acme Corp,87,Manager,Very satisfied with the service.
   Jane Smith,janesmith@example.com,555-0101,Orbit Inc,92,Director,Great product, will recommend!
   ...
    ```
4. Input: The application reads survey data from the `input/` directory. Make sure this directory exists or update the input paths in the code.
5. Logging: Logs are written to the `logs/` directory. Ensure this directory exists or update the logging configuration in the code.
6. Output: The application generates output files in the `output/` directory. Make sure this directory exists or update the output paths in the code.

## Usage

Run the script with:

```bash
python main.py
```

This command executes the `main()` function, which processes the input CSV file and interacts with Monday.com.