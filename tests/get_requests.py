import pytest
import requests
import json


@pytest.mark.parametrize("pair_id", [i for i in range(1, 500)])
def test_stat_requests(pair_id):
    """
    Tests if stat request returns OK
    :param pair_id: id of the pair
    """
    url = "http://0.0.0.0:80/stat"  # url for the request
    response = requests.get(url + "?pair_id=" + str(pair_id))  # getting response
    assert response.status_code == 200  # checks if OK


@pytest.mark.parametrize("pair_id", [i for i in range(1, 400)])
def test_get_top_requests(pair_id):
    """
    Tests if get_top request returns OK and a list of links
    :param pair_id: id of the pair
    """
    url = "http://0.0.0.0:80/get_top"  # url for the request
    response = requests.get(url + "?pair_id=" + str(pair_id))  # getting response
    assert response.status_code == 200  # checks OK status
    assert len(response.json()["result"]) <= 5  # checks number of links

