# Description for the test task

## Environment

platform: linux, Python 3.6.9, pytest 6.0.1, pytest-sugar 0.9.4
plugins: sugar-0.9.4, xdist-2.1.0, forked-1.3.0, cov-2.10.1

## Launch conditions
Required modules:

    pip3 install docker
    pip3 install pytest
    pip3 install allure-pytest

Required programs:
    
    sudo apt-get install python3.6
    sudo apt-get install python-pytest
    sudo apt-get install docker.io
    sudo apt-get install allure

Test launch string:
    
    sudo python3.6 -m pytest rest_api_test.py --alluredir=allure-results

## Test Application Specifications

Due to the fact that the basic specifications are not complete enough, 
I made the following additions:

**Specification of formats and database records for keys:**

bear_name:
    
    accepted formats: str
    range: 1 <= name <= 10
    database storage format: str
    conversion: when saving to the database, converts the string to uppercase
    
bear_age:
    
    accepted formats: int, float
    range: 0 < age <= 100
    database storage format (conversion): float
    
bear_id:

    database storage format: int
    created automatically by the server when a new record is added, 
    each new bear_id differs from the previous one by 1.
    Cannot be changed

**Specifications of expected application responses to client requests:**

    200 - OK
    400 - The request from the client contains invalid values
    404 - Non-existent information is requested (non-existent records in the database)

## Test directory structure:

api.py:

    ApiClient class conists of api methods for application tests
    validate_response_code function to assert response's status codes

constants.py:

    Global test task constants

conftest.py:

    FIXTURE use_docker(scope='session', autouse=True):
        Sturtup: run container, check connectivity
        Teardown: stop and remove container

README.md: 

    Description for the test task, specifications, tests
        
requirements.txt
    
    requirements.txt
     
rest_api_test.py:
    
    FIXTURE api_bear:
        API interfaces
    FIXTURE smoke_test(scope='class'):
        Sturtup: Minimum functional check before testing
    FIXTURE clear(scope='function'):
        Sturtup: cleaning the database before each test
    FIXTURE create_simple_bear:
        Creates simple bear record in database
    CLASS TestAlaska:
        testsuit, containing the whole test suite

## Описание тест кейсов
_NOTE: due to the fact that most of the invalid requests receive a 200 OK response, 
most negative tests have added checks not only for the expected response code, 
but also for the fact that the response code is not 200 OK_


Positive bear POST create + GET read specific bear
    
    Autotest name: test_positive_create_get_bear
    Input data: valid combinations of bear_type, bear_name и bear_age values
    Steps: 
        create configuration json
        send REST Post to create a record in database
    Expected result:
        response code 200
        the created record matches the expected 
        data types in database correspond to the expected
    
Check proper bear bear_id incrementation
    
    Autotest name: test_positive_bear_id_incrementation_create_bear
    Input data: None
    Steps: 
        create first record
        create second record
    Expected result
        bear_id of the second bear differs from bear_id of the first one by 1

Negative bear POST create. WRONG bear_type
    
    Autotest name: test_negative_create_bear_types
    Input data: list of invalid bear_type values
    Steps: 
        send REST Post to create a record
    Expected result:
        response code not 200
        response code 400

Negative bear POST create. WRONG bear_name
    
    Autotest name: test_negative_create_bear_names
    Input data: list of invalid bear_name values 
    Steps: 
        send REST Post to create a record
    Expected result:
        response code not 200
        response code 400

Negative bear POST create. WRONG bear_age
    
    Autotest name: test_negative_create_bear_ages
    Input data: list of invalid bear_age values 
    Steps: 
        send REST Post to create a record
    Expected result:
        response code not 200
        response code 400

Negative bear POST create. Set bear_id by client
    
    Autotest name: test_negative_create_bear_user_ids
    Input data: None
    Steps: 
        send REST Post to create a record
    Expected result:
        response code not 200
        response code 400
        record not created

Negative SPECIFIC bear GET read
    
    Autotest name: test_negative_get_bear
    Input data: list of nonexistent and invalid bear_id
    Steps: 
        send REST Get bear_id from the list
    Expected result
        response code 404, если bear_id - int 
        response code 400, если bear_id - not int

Positive check Delete One bear
    
    Autotest name: test_positive_delete_one_bear
    Input data: None
    Steps: 
        create record
        delete record
        query deleted record
    Expected result
        response code 200 to delete a record
        record does not exist when trying to query

Negative check Delete One non-existent bear
    
    Autotest name: test_negative_delete_one_bear
    Input data: None
    Steps: 
        send REST Delete non-existent record
    Expected result
        response code 404

Positive check Get All + Delete All bears
    
    Autotest name: test_positive_get_all_delete_all_bears
    Input data: None
    Steps: 
        create 10 records
        get whole batabase by get_all request
        clear batabase (delete all records)
    Expected result
        number of records in database == 10
        база данных пуста

Positive bear Update all items
    
    Autotest name: test_positive_update_specific_bear_all
    Input data: valid combinations of bear_type, bear_name and bear_age values
    Steps: 
        create record
        send a REST Update to change the record
    Expected result:
        response code 200
        запись изменена

Negative bear Update. WRONG bear_type
    
    Autotest name: test_negative_update_specific_bear_type
    Input data: list of invalid bear_type values 
    Steps: 
        create record
        send a REST Update to change the record
    Expected result:
        record is not changed
        response code not 200
        response code 400
        
Negative bear Update. WRONG bear_name
    
    Autotest name: test_negative_update_specific_bear_name
    Input data: list of invalid bear_name values 
    Steps: 
        create record
        send a REST Update to change the record
    Expected result:
        record is not changed
        response code not 200
        response code 400
    
    
Negative bear Update. WRONG bear_age
    
    Autotest name: test_negative_update_specific_bear_age
    Input data: list of invalid bear_age values 
    Steps: 
        create record
        send a REST Update to change the record
    Expected result:
        record is not changed
        response code not 200
        response code 400
    
Proof that there is no possibility to change bear_id by Update
    
    Autotest name: test_negative_update_specific_bear_id
    Input data: None
    Steps: 
        create record
        send a REST Update to change the record
    Expected result:
        record is not changed
        response code not 200
        response code 400
    
Negative http incorrect header check
    
    Autotest name: test_negative_use_incorrect_header
    Input data: list of invalid headers for REST requests
    Steps: 
        send a REST Post to create the record
    Expected result:
        record not created
        response code not 200
        response code 400