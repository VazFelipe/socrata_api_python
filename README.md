# The script provides studies about API requests.

## The proof of concept - phase 1

> request_socrata_soda.py ingest data from Police Department Incident Reports in a JSON form and load into a bucket using parameters to define the start incident_datetime and the number_of_days desired. The idea is for testing the processing and reprocessing feature.

> extract_load_data(bucket_name=YOUR BUCKET NAME, start_date=start_date, number_of_days=DESIRED integer) is the function that you'll use to run this code and in the line 15 to 19 there's some static variables to play with.

> to run this code you'll need to provide a config.json that wasn't provided here. If you want to run, just clone and follow this dictionary:

```
{
    "api":{
        "domain": {
            "url": "https://data.sfgov.org/resource/"
        },
        "dataset": {
            "san_francisco_data": "wg3w-h783"
        },
        "credentials": {
            "username": "your username from Socrata",
            "password": "your password from Socrata"
        },
        "headers": {
            "X-App-Token": "App token from Socrata Api",
            "Content-type": "application/json"
        }
    },
    "gcp":{
        "credentials":{
            "folder": "GCP service_account from your directory"
        }
    }
}
```

> to get the credentials for data extraction visit https://dev.socrata.com/docs/endpoints.html and follow the instructions.

> to get credentials for data storage visit https://cloud.google.com/free?hl=pt-br and follow the instructions.

> in the files folder you'll see files from this code in csv and JSON format. Use the socrata_2018-01-01_dataset_wg3w-h783_crimes_in_loaded_1682068024187410300.json to see the results, because the others are only test.

> in the guidance folder you'll see studies from Corey Shaffer channel on https://youtu.be/tb8gHvYlCFs.

> in the trials folder you'll see some free coding.

> this codes has many to dos, so do not hesitate in criticize. Although, I'll not provide any update on it, just learn from your thoughts.

### Raw data from Police Department Incident Reports

> more details in: https://dev.socrata.com/foundry/data.sfgov.org/wg3w-h783

### Architecture

- I'm using Google Cloud Platform for this project
- Basically, Request from API and storage on Cloud Storage :::**DONE**::: and then staging on BigQuery :::**TO DO**:::
- The topology will be Raw :::**DONE**::: > Staging :::**TO DO**::: > Master Data :::**TO DO**:::

### Ideas behind the scenes

> more details in: https://www.ibm.com/garage/method/practices/code/construct-data-topology/

## The Raw in production using Python best practices: classes - phase 2

> in this phase I'll study and implement classes to organize and make this code more readable, reusable and scalable :::**TO DO**:::

> My thoughts about the classes diagram looks like:

```
api_socrata
	connection
		logs
	latency and throughput
	
cloud_storage
	connection
		logs
	latency and throughput

data_extraction_loading
	params = start_date, end_date, bucket_name,  
	default = from last date in the bucket
		first load = from the minimal incident_datetime in the api data
	reprocess = from the user range 
		mode = batch or full
			logs
```


