# Insights on Financial Complaints
Analyze financial complaints to generate insights about them.

## Context
Provide insights for an imaginary company that deal with customer complaints and offers
its service to companies in the financial sector and is looking for new customers.

### Assumptions
* Neither constraints nor service prices are known.
* Prospect big customers is time-consuming strategy, thus the plans can not change. 
  The analysis is one time shot and realtime data is not a necessity.
* Short term tendencies only, therefore data was filtered (>= 2018) or open complaints.

## Goal
Shortlist potential customers considering different criteria.

## Data
It is a dataset with microdata of complaints recorded by The Consumer Financial Protection Bureau with no
numeric variables in it. The SQL schema showed 18 variables, but in some of them there is a majority of NA's.

CFPB - BigQuery Public Data

Selected variables: 

>date_received                   (datetime)  
product                         (str)  
subproduct                      (str)  
issue                           (str)  
company_name                    (str)  
company_response_to_consumer    (str)  
timely_response                   (bool)  
complaint_id                    (str)  
date_received                   (datetime)  
product                         (str)  
subproduct                      (str)  
issue                           (str)  
company_name                    (str)  
company_response_to_consumer    (str)
complaint_id                    (str)  


## Deliverable
https://caio-fin-complaints.herokuapp.com/

### Some questions that guided the investigation
Which companies have the most monthly complaints?  
Are these companies the same ones that delay responses?
Is the company with the most complaints the one with most 'In progress' status?
How are the types of complaints distributed? Are companies 'specialized' in certain complaints?
How can companies be shortlisted?

## Author
Caio Mescouto Terra de Souza

    email: caiomescouto@gmail.com

## Version History

* 0.1.
    * Initial release:
    
## License
This project is licensed under the MIT License - see the LICENSE.md file for details






