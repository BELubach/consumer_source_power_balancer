from httpx import AsyncClient
import pytest

@pytest.mark.e2e
class TestConsumersListEndpoint:

    async def test_get_consumers(self,
                    client: AsyncClient):
        
        response = await client.get("/api/v1/consumers")
        # loaded data from consumers.json should be available in the db 
        assert response.status_code == 200

        consumers = response.json()
        assert len(consumers) == 6
        assert consumers[0]["name"] == "Hospital Complex"
        assert consumers[0]["priority"] == 1
        assert consumers[0]["active_power"] == 200
        assert len(consumers[0]["required_power"]) == 2
        assert consumers[0]["required_power"][0]["source_id"] == 1
        assert consumers[0]["required_power"][0]["capacity"] == 100
        assert consumers[0]["required_power"][0]["is_active"] == True
        assert consumers[0]["required_power"][1]["source_id"] == 4
        assert consumers[0]["required_power"][1]["capacity"] == 100
        assert consumers[0]["required_power"][1]["is_active"] == True
        assert consumers[1]["name"] == "Data Center"
        assert consumers[1]["priority"] == 2
        assert consumers[1]["active_power"] == 250
        assert len(consumers[1]["required_power"]) == 2
        assert consumers[1]["required_power"][0]["source_id"] == 2
        assert consumers[1]["required_power"][0]["capacity"] == 150
        assert consumers[1]["required_power"][0]["is_active"] == True
        assert consumers[1]["required_power"][1]["source_id"] == 5
        assert consumers[1]["required_power"][1]["capacity"] == 100
        assert consumers[1]["required_power"][1]["is_active"] == True
        assert consumers[2]["name"] == "Manufacturing Plant"
        assert consumers[2]["priority"] == 3
        assert consumers[2]["active_power"] == 350
        assert len(consumers[2]["required_power"]) == 2
        assert consumers[2]["required_power"][0]["source_id"] == 3
        assert consumers[2]["required_power"][0]["capacity"] == 200
        assert consumers[2]["required_power"][0]["is_active"] == True
        assert consumers[2]["required_power"][1]["source_id"] == 4
        assert consumers[2]["required_power"][1]["capacity"] == 150
        assert consumers[2]["required_power"][1]["is_active"] == True
        assert consumers[3]["name"] == "Residential District"
        assert consumers[3]["priority"] == 2
        assert consumers[3]["active_power"] == 130
        assert len(consumers[3]["required_power"]) == 2
        assert consumers[3]["required_power"][0]["source_id"] == 1
        assert consumers[3]["required_power"][0]["capacity"] == 80
        assert consumers[3]["required_power"][0]["is_active"] == True
        assert consumers[3]["required_power"][1]["source_id"] == 6
        assert consumers[3]["required_power"][1]["capacity"] == 50
        assert consumers[3]["required_power"][1]["is_active"] == True
        assert consumers[4]["name"] == "Shopping Mall"
        assert consumers[4]["priority"] == 4
        assert consumers[4]["active_power"] == 125
        assert len(consumers[4]["required_power"]) == 2
        assert consumers[4]["required_power"][0]["source_id"] == 2
        assert consumers[4]["required_power"][0]["capacity"] == 50
        assert consumers[4]["required_power"][0]["is_active"] == True
        assert consumers[4]["required_power"][1]["source_id"] == 5
        assert consumers[4]["required_power"][1]["capacity"] == 75
        assert consumers[4]["required_power"][1]["is_active"] == True
        assert consumers[5]["name"] == "Train Station"
        assert consumers[5]["priority"] == 1
        assert consumers[5]["active_power"] == 150
        assert len(consumers[5]["required_power"]) == 2
        assert consumers[5]["required_power"][0]["source_id"] == 3
        assert consumers[5]["required_power"][0]["capacity"] == 100
        assert consumers[5]["required_power"][0]["is_active"] == True
        assert consumers[5]["required_power"][1]["source_id"] == 6
        assert consumers[5]["required_power"][1]["capacity"] == 50
        assert consumers[5]["required_power"][1]["is_active"] == True

    
    async def test_get_consumers_filtered_by_priority(self,
                    client: AsyncClient):
        response = await client.get("/api/v1/consumers?priority_gte=3")
        # priority 3, so only Manufacturing Plant and Shopping Mall should be returned

        assert response.status_code == 200
        consumers = response.json()
        assert len(consumers) == 2
        assert consumers[0]["name"] == "Manufacturing Plant"
        assert consumers[1]["name"] == "Shopping Mall"
        
  
    async def test_get_consumers_exclude_power_details(self,
                    client: AsyncClient):
        response = await client.get("/api/v1/consumers?include_power_details=false")
        # nestd required_power objects should not be included in the response 

        assert response.status_code == 200
        consumers = response.json()
        assert len(consumers) == 6
        assert consumers[0]["name"] == "Hospital Complex"
        assert consumers[0]["required_power"] == None
        assert consumers[1]["name"] == "Data Center"
        assert consumers[1]["required_power"] == None
        assert consumers[2]["name"] == "Manufacturing Plant"
        assert consumers[2]["required_power"] == None
        assert consumers[3]["name"] == "Residential District"
        assert consumers[3]["required_power"] == None
        assert consumers[4]["name"] == "Shopping Mall"
        assert consumers[4]["required_power"] == None
        assert consumers[5]["name"] == "Train Station"
        assert consumers[5]["required_power"] == None
        


@pytest.mark.e2e
class TestDeactivateByPriorityEndpoint:

    async def test_deactivate_by_priority(self,
                    client: AsyncClient):
        
        response = await client.post("/api/v1/consumers/deactivate-by-priority", 
                                    json={"priority_threshold": 4})
        # priority 4 => shopping mall should be disabled (item 5 in the list of consumers)

        assert response.status_code == 200

        consumers = response.json()
        assert consumers[0]['active_power'] == 200
        assert consumers[1]['active_power'] == 250
        assert consumers[2]['active_power'] == 350
        assert consumers[3]['active_power'] == 130
        assert consumers[4]['active_power'] == 0             
        assert consumers[5]['active_power'] == 150

    
    async def test_deactivate_by_priority_2(self,
                    client: AsyncClient):
        
        response = await client.post("/api/v1/consumers/deactivate-by-priority", 
                                    json={"priority_threshold": 2})
        # priority 2 => all but hospital and train disabled

        assert response.status_code == 200

        consumers = response.json()
        assert consumers[0]['active_power'] == 200
        assert consumers[1]['active_power'] == 0
        assert consumers[2]['active_power'] == 0
        assert consumers[3]['active_power'] == 0
        assert consumers[4]['active_power'] == 0             
        assert consumers[5]['active_power'] == 150


    
    async def test_deactivate_by_priority_no_match(self,
                    client: AsyncClient):
        
        response = await client.post("/api/v1/consumers/deactivate-by-priority", 
                                    json={"priority_threshold": 5})
        # priority 5 => no consumer should be disabled

        assert response.status_code == 200

        consumers = response.json()
        assert consumers[0]['active_power'] == 200
        assert consumers[1]['active_power'] == 250
        assert consumers[2]['active_power'] == 350
        assert consumers[3]['active_power'] == 130
        assert consumers[4]['active_power'] == 125          
        assert consumers[5]['active_power'] == 150


@pytest.mark.e2e
class TestUpdateConsumerPowerEndpoint:

    async def test_update_consumer_power(self,
                    client: AsyncClient):
        
        response = await client.patch("/api/v1/consumers/2", 
                                    json={"is_active": False})
        # consumer 2 is data center

        assert response.status_code == 200

        consumer = response.json()
        assert consumer['name'] == "Data Center"
        assert consumer['active_power'] == 0
        assert len(consumer['required_power']) == 2
        assert consumer['required_power'][0]['capacity'] == 150
        assert consumer['required_power'][0]['is_active'] == False
        assert consumer['required_power'][1]['capacity'] == 100
        assert consumer['required_power'][1]['is_active'] == False

    async def test_update_consumer_power_not_found(self,
                    client: AsyncClient):
        
        response = await client.patch("/api/v1/consumers/999", 
                                    json={"is_active": False})
        # consumer 999 does not exist, should return 404

        assert response.status_code == 404