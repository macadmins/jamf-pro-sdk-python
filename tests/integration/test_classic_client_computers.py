import random


def test_integration_classic_get_computers(jamf_client):
    result_list = jamf_client.classic_api.list_all_computers(subsets=["basic"])

    # Select five records at random, read, and verify their IDs
    for _ in range(0, 5):
        listed_computer = random.choice(result_list)
        computer_read = jamf_client.classic_api.get_computer_by_id(listed_computer.id)

        assert computer_read.general.id == listed_computer.id
        assert computer_read.general.udid == listed_computer.udid
        assert computer_read.general.name == listed_computer.name
        assert computer_read.general.mac_address == listed_computer.mac_address
