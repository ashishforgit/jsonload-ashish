# Script Requirements
1. `Python 3.6.9`
2. Python Packages
   1. Required: `pandas==0.25.3`
   2. Optional: `sqlalchemy==1.3.13`

> Note: How to install these packages on Windows PyCharm can be seen [here](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html).


# Project Questions

1. **Please provide instructions on how to run the script.**<br>
   
   It depends on which operating system you are using.<br> 
   The simplest way to do so is just install PyCharm, install the required packages mentioned above and run using pycharm.<br>
   I will still specify on how to run on `Ubuntu`
   #### How to run on `Ubuntu`?
   1. Install Python by running on terminal:
      ```
      $ sudo apt install python3.6
      ```
   2. Install `pip`
      ```
      $ sudo apt install python3-pip
      ```
   3. Install required package(s)
      ```
      $ pip3 install pandas==0.25.3
      ```
   4. Specify the path to the `json` data file and output dump folder in Python against variables `JSON_FILE_LOCATION` & `OUTPUT_FILE_PATH` respectively.
   5. Run Python script
      ```
      $ python3 json-load.py
      ```
   6. See output
      Go to the folder specified in variable `OUTPUT_FILE_PATH` and there will be an `output.csv` there.
2. **How would you design the ETL process for it to automatically update daily? How would you scale this process if we got tens or hundreds of millions of events per day? Suggest any target architecture to cater for this growth?**

    First of all, we can make these events into a data stream using [`Apache Kafka`](https://kafka.apache.org/) or other data streaming service.<br><br>
Then we can use `Apache Spark` (or its python flavour `Pyspark`) or `Apache Flink` to process that real time streaming data no matter how large it grows because all three of `Apache Spark`, `Apache Flink` and `Apache Kafka` are horizontally scalable.
There’s even an AWS service for Apache Spark auto scale clusters, called AWS EMR.

    So architecture would be pretty straightforward:<br><br>
   1. We send data to stream using possibly kafka.<br>
   2. We connect our apache spark / pyspark or apache flink to connect to the source and do our ONE TIME written transformation with the continually updating stream.

    One other possible architecture could be that;
    1. We keep dumping our data (events) in a database.
    2. We write a one time ETL like the attached script and schedule it to run periodically at desired intervals using a crone job or `Apache Airflow`. 

    > Note that the second possible architecture does not process data in REAL TIME, but on the other hand, it also does not use the streaming data as source.
