from httpx import AsyncClient
import pytest

@pytest.mark.e2e
class TestSourcesListEndpoint:

    async def test_get_sources(self,
                    client: AsyncClient):
        
        response = await client.get("/api/v1/sources")
        # loaded data from consumers.json should be available in the db 
        assert response.status_code == 200

        sources = response.json()
        assert len(sources) == 6
        assert sources[0]["name"] == "Solar Farm Alpha"
        assert sources[0]["capacity"] == 150
        assert sources[1]["name"] == "Wind Turbine Park Beta"
        assert sources[1]["capacity"] == 200
        assert sources[2]["name"] == "Hydroelectric Plant Gamma"
        assert sources[2]["capacity"] == 300
        assert sources[3]["name"] == "Nuclear Reactor Delta"
        assert sources[3]["capacity"] == 500
        assert sources[4]["name"] == "Gas Turbine Epsilon"
        assert sources[4]["capacity"] == 250
        assert sources[5]["name"] == "Battery Storage Zeta"
        assert sources[5]["capacity"] == 100


