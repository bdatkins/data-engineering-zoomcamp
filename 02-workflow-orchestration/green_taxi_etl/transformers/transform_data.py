if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    print("Rows with zero passengers", data['passenger_count'].isin([0]).sum())
    print("Rows with zero length trips", data['trip_distance'].isin([0]).sum())

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    data.rename(columns = {
        "VendorID": "vendor_id",
        "RatecodeID" : "rate_code_id",
        "PULocationID" : "pu_location_id",
        "DOLocationID" : "do_location_id",
    }, inplace=True)

    return data[(data['passenger_count']>0) & (data['trip_distance']> 0.0)]

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert ~output['passenger_count'].isin([0]).any()
    assert ~output['trip_distance'].isin([0]).any()
    assert output['vendor_id'].isin([1,2]).any()
