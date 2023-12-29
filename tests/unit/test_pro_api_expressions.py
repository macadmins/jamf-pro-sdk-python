from datetime import datetime

from src.jamf_pro_sdk.clients.pro_api.pagination import (
    # FilterEntry,
    # FilterExpression,
    FilterField,
    # SortExpression,
    SortField,
    filter_group,
)

STRF_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def test_basic_filter_expression():
    expression = FilterField("id").eq(1)
    assert str(expression) == "id==1"


def test_multiple_filter_expression():
    expression1 = FilterField("expires").gte(
        datetime(year=2023, month=9, day=11, hour=14).strftime(STRF_TIME_FORMAT)
    ) & FilterField("expires").lte(
        datetime(year=2023, month=9, day=11, hour=15).strftime(STRF_TIME_FORMAT)
    )

    assert str(expression1) == "expires>=2023-09-11T14:00:00Z;expires<=2023-09-11T15:00:00Z"


def test_in_out_filter_expressions():
    expression1 = FilterField("status").is_in(["PENDING", "ACKNOWLEDGED"])
    assert str(expression1) == "status=in=(PENDING,ACKNOWLEDGED)"

    expression2 = FilterField("status").not_in(["NOT_NOW", "ERROR"])
    assert str(expression2) == "status=out=(NOT_NOW,ERROR)"


def test_jamf_dev_docs_example_filter_expression():
    # TODO: Spaces and special character handling using quotes
    expression = filter_group(
        FilterField("general.barcode1").eq("Sample") | FilterField("general.barcode2").eq("Sample")
    ) & FilterField("general.assetTag").gt(20)

    # assert (
    #     str(expression)
    #     == '(general.barcode1=="Sample",general.barcode2=="Sample");general.assetTag>"20"'
    # )
    assert (
        str(expression) == "(general.barcode1==Sample,general.barcode2==Sample);general.assetTag>20"
    )


def test_sort_field_expressions():
    expression1 = SortField("name").asc()
    assert str(expression1) == "name:asc"

    expression2 = SortField("id").desc()
    assert str(expression2) == "id:desc"

    expression3 = SortField("date").desc() & SortField("name").asc()
    assert str(expression3) == "date:desc,name:asc"
