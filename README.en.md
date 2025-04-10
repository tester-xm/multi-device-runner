Description
multi-device-runner is a tool designed for parallel testing on multiple devices. It can simultaneously execute Airtest scripts on multiple Android devices and generate detailed test reports. The main features include:
Multi-device Parallel Testing
It supports running Airtest scripts on multiple Android devices concurrently, significantly enhancing testing efficiency.
Log Recording and Management
It records the test logs of each device and provides functions for log cleaning and copying.
Test Report Generation
It generates HTML-formatted test reports for each device and aggregates the test results.
Log Parsing and Excel Generation
It parses the device log files and organizes the log content into Excel files.
Installation Dependencies
Before running multi-device-runner, you need to install the required Python dependencies. You can install them using the following command:
bash
pip install -r requirements.txt
The requirements.txt file contains all the necessary dependencies, which are as follows:
airtest: The Airtest testing framework, used for writing and executing automated test scripts.
pandas: A Python library for data processing and analysis.
openpyxl: A Python library for operating Excel files.
pywin32: A Python library for operating files and folders on the Windows platform.
Software Deployment
Step 1: Connect Android Devices
Ensure that all Android devices to be tested are connected to the computer via USB and that USB debugging mode is enabled.
Step 2: Prepare Airtest Scripts
Place the Airtest scripts you want to run in the multi-device-runner directory. For example, start_run_stop.air.
Step 3: Run Tests
Navigate to the multi-device-runner directory in the terminal and run the following command:
bash
python run.py
If you need to re-run all scripts, use the following command:
bash
python run.py --run_all
Step 4: View Test Reports
After the tests are completed, HTML-formatted test reports will be generated in the log directory of each device. Additionally, a summary report named report.html will be generated in the project root directory. You can open these report files using a browser to view detailed test results.
Notes
Make sure that the ADB tool is installed on your computer and that the ADB environment variables are correctly configured.
Before running the tests, it is recommended to clean the device log buffer to avoid interference from old logs on the test results. You can use the clean_log_files function to clean the log files.