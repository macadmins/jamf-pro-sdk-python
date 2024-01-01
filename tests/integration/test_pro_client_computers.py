# from jamf_pro_sdk.clients.pro_api.pagination import FilterField, SortField


def test_integration_pro_computer_inventory_v1_default(jamf_client):
    # This test is only valid if the computer inventory is less than the max page size

    # Test at max page size to get full inventory count
    result_one_call = jamf_client.pro_api.get_computer_inventory_v1(page_size=2000)
    result_total_count = len(result_one_call)
    assert result_total_count > 1

    # Test paginated response matches full inventory count above
    result_paginated = jamf_client.pro_api.get_computer_inventory_v1(page_size=10)
    assert result_total_count == len(result_paginated)
