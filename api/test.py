from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_bad_endpoint():
    response = client.get("/non-existent-endpoint")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_life_expectancy():
    response = client.get("/life_expectancy/Male/White/2010")
    assert response.status_code == 200
    assert response.json() == {"average_life_expectancy": 76.5}

def test_life_expectancy_bad_request():
    response = client.get("/life_expectancy/Male/Another/2010")
    assert response.status_code == 200
    assert response.json() == {"error": "Sex or Race are not included in the available ones"}

def test_life_expectancy_no_data():
    response = client.get("/life_expectancy/Male/White/2018")
    assert response.status_code == 200
    assert response.json() == {"error": "Without Data"}

def test_unemployment():
    response = client.get("/unemployment/Alabama")
    assert response.status_code == 200
    assert response.json() == {"rate": 14.9}

def test_life_expectancy_no_data():
    response = client.get("/unemployment/Not a State")
    assert response.status_code == 200
    assert response.json() == {"error": "State not found"}

def test_trends():
    response = client.get("/trends?phrase=hello world&start_date=2022-06-17&end_date=2022-07-01")
    assert response.status_code == 200
    assert response.json() == {"interest": [56,72,75,70,69,79,80,76,78,73,62,59,67,68,59,58,52,50,47,50,50,50,48,49,52,54,63,56,61,63,67,54,60,57,50,48,49,66,49,55,52,47,51,43,43,45,47,48,48,54,49,57,66,59,60,55,55,57,51,54,50,57,42,50,47,49,48,45,46,45,51,54,53,58,67,73,75,76,75,77,85,82,67,63,64,57,70,55,53,52,54,50,47,52,56,56,57,60,74,74,69,75,88,83,88,74,75,54,56,70,58,61,55,48,51,56,51,46,53,59,63,51,64,67,76,73,85,86,79,70,65,65,67,73,65,61,59,54,55,54,59,51,48,55,48,51,76,61,82,79,100,78,88,85,76,59,71,67,61,59,59,50,57,53,55,49,59,55,48,54,67,77,70,76,81,88,71,85,84,68,67,71,65,68,62,58,57,60,56,52,51,52,59,55,57,59,62,63,73,83,62,68,62,58,55,56,52,44,51,59,54,56,47,43,48,59,49,47,51,53,60,69,70,65,60,60,60,70,63,58,60,55,52,59,52,47,45,53,55,60,57,52,71,78,79,81,87,75,78,84,83,76,71,72,63,69,69,63,63,62,54,59,59,51,63,69,69,83,76,84,94,94,87,100,83,77,69,77,82,73,71,62,67,58,53,57,63,67,67,66,71,81,82,92,100,97,92,83,96,91,68,81,78,87,68,67,64,64,61,61,65,75,64,72,65,78,73,92,80,90,87,83,84,78,68,72,75,68,79,64,68,66,53,66,60,53,69,60,69]}

def test_trends_without_parameters():
    response = client.get("/trends")
    assert response.status_code == 200
    assert response.json() == {"error": "A phrase is required or dates are badformed (Correct way: YYYY-mm-dd)"}

def test_trends_bad_dates_formation():
    response = client.get("/trends?phrase=hello world&start_date=17/06/2022&end_date=01/07/2022")
    assert response.status_code == 200
    assert response.json() == {"error": "A phrase is required or dates are badformed (Correct way: YYYY-mm-dd)"}
    
def test_trends_weather_without_phrase():
    response = client.get("/trends")
    assert response.status_code == 200
    assert response.json() == {"error": "A phrase is required"}