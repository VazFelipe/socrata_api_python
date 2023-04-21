# The script provides studies about API requests.

## The proof of concept

> request_socrata_soda.py ingest data from Police Department Incident Reports in a JSON form and load into a bucket using parameters to define the start incident_datetime and the number_of_days desired. The idea is for testing the processing and reprocessing feature.

> extract_load_data(bucket_name=YOUR BUCKET NAME, start_date=start_date, number_of_days=DESIRED integer) is the function that you'll use to run this code and in the line 15 to 19 there's some statics variables to play with.

> To run this code you'll need to provide a config.json that wasn't provided here. If you want to run, just clone and follow this dictionary


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

> To get the credentials for data extraction visit https://dev.socrata.com/docs/endpoints.html and follow the instructions.

> This codes has many to dos, so do not hesitate in criticize. Although, I'll not provide any update on it. Just learn from your thoughts.

## Raw data from Police Department Incident Reports

> more details in: https://dev.socrata.com/foundry/data.sfgov.org/wg3w-h783

## Architecture

- I'm using Google Cloud Platform for this project
- Basically, Cloud Storage and BigQuery DONE
- The topology will be Raw > Staging > Master Data TO DO

## Ideas behind the scenes

> more details in: https://www.ibm.com/garage/method/practices/code/construct-data-topology/