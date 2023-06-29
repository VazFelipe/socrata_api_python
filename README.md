# Personal Project: Data Engineering Lifecycle

## Contents

- [The San Francisco Police Department dataset](#the-police-department-incident-reports)
- [The raw ingestion phase 1 FP](#the-raw-ingestion-using-python-functional-programming-best-practices-phase-1)
- [The raw ingestion phase 2 OOP](#the-raw-ingestion-using-python-best-practices-classes---phase-2)
- [The medallion architecture phase 3](#the-development-of-medallion-architecture-in-azure-platform---phase-3)
- [The raw ingestion in Azure](#01-raw)
- [The silver layer in Azure](#02-silver)
- [The data profiling in silver layer](#data-profiling)
- [Asking for help in a team scenario](#collaboration)
- [Pit stop for Cost and Performance Optimization](#pit-stop-for-cost-and-performance-optimization)
- [The gold layer in Azure](#03-gold)
- [The delivering of metrics](#the-metrics-panel--doing)

## The Police Department Incident Reports

_"The San Francisco Police Department’s (SFPD) Incident Report Datatset is one of the most used datasets on DataSF. The dataset compiles data from the department’s Crime Data Warehouse (CDW) to provide information on incident reports filed by the SFPD in CDW, or filed by the public with the SFPD."_

> More details in [here](https://dev.socrata.com/foundry/data.sfgov.org/wg3w-h783) and [here](https://datasf.gitbook.io/datasf-dataset-explainers/sfpd-incident-report-2018-to-present).

[get back to contents](#contents)

## Architecture

- I'm using Python as language and Cloud Platforms like Google Cloud and Azure
- Basically, I'm requesting data from API and storage it on Cloud Storage (Phase 1 and 2) :::**DONE**::: 
- Then in the Phase 3 I'll start developing on Azure Plarform using the medallion architecture :::**DOING**:::
- The data layers will be Bronze :::**DONE**::: > Silver :::**DOING**::: > Gold :::**TO DO**:::

## Ideas behind the scenes

> More details in: https://www.ibm.com/garage/method/practices/code/construct-data-topology/ and
> https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion

## The Raw ingestion using Python Functional Programming best practices: phase 1

> Request_socrata_soda.py ingest data from Police Department Incident Reports in a JSON form and load into a bucket using parameters to define the start incident_datetime and the number_of_days desired. The idea is for testing the processing and reprocessing feature.

> Extract_load_data(bucket_name=YOUR BUCKET NAME, start_date=start_date, number_of_days=DESIRED integer) is the function that you'll use to run this code and in the line 15 to 19 there's some static variables to play with.

> To run this code you'll need to provide a config.json that wasn't provided here. If you want to run, just clone and follow this dictionary:

![](/phase_1/images/config_json_phase_1.png)

> To get the credentials for data extraction visit https://dev.socrata.com/docs/endpoints.html and follow the instructions.

> To get credentials for data storage visit https://cloud.google.com/free?hl=pt-br and follow the instructions.

> In the files folder you'll see files from this code in csv and JSON format. Use the socrata_2018-01-01_dataset_wg3w-h783_crimes_in_loaded_1682068024187410300.json to see the results, because the others are only test.

> In the guidance folder you'll see studies from Corey Shaffer channel on https://youtu.be/tb8gHvYlCFs.

> In the trials folder you'll see some free coding.

> This codes has many to dos, so do not hesitate in criticize. Although, I'll not provide any update on it, just learn from your thoughts.

[get back to contents](#contents)

## The Raw ingestion using Python best practices: classes - phase 2

> In this phase I'll study and implement classes to organize and make this code more readable, reusable and scalable :::**DONE**:::

> My thoughts about the classes diagram looks like:

![](/phase_2/images/classes_diagram.png)

[get back to contents](#contents)

## The development of medallion architecture in Azure Platform - phase 3

### San Francisco Police Department Data Dictionary

> This dictionary below was developed for the stakeholders, business analysts and people interested in get a nice understanding about what represents every aspect of the Police Department Data, the underlying structure and datatypes. Later in this project it will be rollout to Purview, a Data Governance Application [here](https://azure.microsoft.com/en-us/products/purview).

![](/phase_3/images/data_dictionary.png)

### 01-raw

> This parameterized template developed here ingest raw data from the City and County of San Francisco using Socrata Open Data API. The San Francisco Police Department's (SFPD) Incident Report Dataset is one of the most used reports for crime analysis. See the literature [here](https://www.sanfranciscopolice.org/sites/default/files/2022-11/SFPDQADRReport-2ndQuarter-20221129.pdf) and [here](https://scholar.google.com.br/scholar?hl=pt-BR&as_sdt=0%2C5&q=The+San+Francisco+Police+Department%E2%80%99s+%28SFPD%29+Incident+Report+Dataset&btnG=).

> The holistic workflow presented below executes everyday at 11AM UTC, flag the trigger time as a watermark and store it in the /execution_logs/01-raw/ingestion_api_socrata.log. Then, the next execution starts from the last execution time in the log. This techinique is well documented [here](https://dwbi1.wordpress.com/2022/05/22/watermark-in-data-warehousing/) and [here](https://learn.microsoft.com/en-us/azure/data-factory/tutorial-incremental-copy-overview). 

**Bronze Layer**

![](/phase_3/images/bronze_layer.png)

> The response from Socrata API is a JSON format and is stored in a hierarchical structure inside the blob storage Gen2 like Year/Month/watermakUnixTimestamp_fieldName_reportGenerationYYYMMDD.json

**Hierarchical Structure in the blob Storage Gen2**

![](/phase_3/images/bronze_hierarchical_structure.png)

[get back to contents](#contents)

### 02-silver

> This parameterized template fetch the data after 10 minutes of the bronze layer pipeline execution, applies the watermark technique storage and writes it in a new column. Then the data is converted to parquet and snappy compressed. The holistic workflow is presented below:

**Silver Layer**

![](/phase_3/images/silver_layer.png)

**Hierarchical Structure in the blob Storage Gen2**

![](/phase_3/images/silver_hierarchical_structure.png)

> In the **silver layer** the data has to be validated, enriched and ready for downstream analytics. **Data profiling technique** was applied using python and pandas library to understand the data types and data patterns for the data quality improvements. The scenario described below shows the evaluation steps that leads to the mapping phase in the pipeline and for the transformations needed to make data available in the right way (at least in my opinion):

#### Data profiling

> The parameters for data analysis ranges from 1 March 2022 until 31 March 2023. The data shape has 149.272 records per 31 columns (20% coverage of total size 735.432). The data_profiling.py has all the code used on it.

**Missing values**

> The nulls in data occurs, and may change over the time, in the fields below:

![](/phase_3/images/silver_data_profiling_missing.png)

> The **'Not applicable' Kimball's rules** [here](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/null-dimension-attribute/) and [here](https://www.kimballgroup.com/2003/02/design-tip-43-dealing-with-nulls-in-the-dimensional-model/) applied for data validation refers to the:

"_Null-valued dimension attributes result when a given dimension row has not been fully populated, or when there are attributes that are not applicable to all the dimension’s rows. In both cases, we recommend substituting a descriptive string, such as Unknown or Not Applicable in place of the null value. Nulls in dimension attributes should be avoided because different databases handle grouping and constraining on nulls inconsistently._"

> The rules for each field can see below:

![](/phase_3/images/data_dictionary_details.png)

> Some rules is in evaluation, see files in **phase_3/business_rules**. There is no specific deadline in this definitions, because this is a study case. Real projects have methodologies for such product evolution, like Agile, Kanban, etc...

> In Azure Data Factory, the missing values replacement was made by applying a Data Flow mapping to the pipeline:

![](/phase_3/images/silver_data_profiling_missing_solved.png)

[get back to contents](#contents)

#### Collaboration
> If I had a PO (Product Onwer) working in this project I would like to ask him:

_**Why incident codes** in 4164, 6351, 6352, 6353, 6354, 6377, 6378, 6399, 7060, 9171, 12020, 12073, 12075, 13072, 15164, 15165, 15410, 27400, 27401, 64100, 65021, 74020, 74022, 74024, 75011 represents 652 incidents that has not category or subcategory? Those incidents have been filed category and subcategory as NA (Not applicable). Is there any business reference to better deliver this value to the business areas?_

_**Why police district** has "Out of SF" category inside the San Francisco boundaries? Using the geo data "All Cases Map View" from Socrata API could solve this latitude and longitude nulls? More details in sfpd_analysis_neighborhood_with_out_of_SF_and_geolocation_nulls.csv. I have applied latitude as 37.774929 and longitude as -122.419416 in case of nulls that represents the San Francisco boundaries._

[get back to contents](#contents)

### Pit Stop for Cost and Performance Optimization

> While working on this amazing project I have facing challenges on cost. Maybe this is due my Pay-As-You-Go tier with Microsoft. I have started my free account and Microsoft gave me 200 dollars and access to monthly free amounts of popular services for 12 months [here](https://azure.microsoft.com/en-in/pricing/offers/ms-azr-0003p/). So, I spend it all, and my first invoice was terrible: R$ 374,00! What did I do wrong? I publish all my work without looking carefully to the cost of services.

> Then, I have started googling and there is amazing references by Arindam [here](https://www.sqlservercentral.com/articles/understanding-azure-data-factory-pricing) and Deepak Goyal [here](https://azurelib.com/how-to-optimize-azure-data-factory-pricing/#Data_Pipelines_on_Azure_Integration_Runtime). In a glimpse, the primary rules: 

- Remove all unused pipeline as they also cost
- Set the DIU to minimum value instead of keeping them as auto. (This could reduce the cost by half)
- Reduce the number of activities if possible

> And the results in cost and performance was terrific:

![](/phase_3/images/cost_performance_optimization.png)

> Take some time to get in touch on this documentation and enjoy a better cost and performance in your projects.

[get back to contents](#contents)

### 03-gold

#### The metrics panel ::: DOING :::

> Using the reporting requirements from the Law Enforcement Agencies, the California Cities reports "_any complaints alleging racial
or identity profiling and detailed demographic data for traffic and pedestrian stops_" since 2016.

> The SFPD dataset provides the most used report and an unique information for police and crime analysis. The incident report filled and displayed in this project was approved by a Sergeant or Lieutenant and does not provide:

- The incident report does not provide information of any person
- The incident report does not provide incidents of juveniles
- The incident report does not provide real location, only the intersection level will be displayed

> The metrics panel will have the opportunity to clearly display daily information for the community regarding the Law Enforcement Agencies requirements.

[get back to contents](#contents)

**The metrics in development are:**

- number of incidents by
    - incident datetime: day, month, year
    - by day of week: sunday-saturday
    - by resolution: open or active, unfounded, citation or arrest
    - by district: SFDP districts
    - by category: for example, Larceny Theft, Assault, Fraud
    - by latitude and longitude: SFDP districts

**The dashboard visual should display:**

![](/phase_3/images/gold_metrics_all.png)

[get back to contents](#contents)
