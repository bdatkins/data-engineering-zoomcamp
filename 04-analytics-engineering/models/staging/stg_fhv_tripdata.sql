{{
    config(
        materialized='view'
    )
}}


with tripdata as 
(
  select *  from {{ source('staging','fhv_tripdata') }}
    where extract(year from  pickup_datetime) = 2019
)

select
    {{ dbt.safe_cast("pulocationid", api.Column.translate_type("integer")) }} as pickup_locationid,
    {{ dbt.safe_cast("dolocationid", api.Column.translate_type("integer")) }} as dropoff_locationid,
    
    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(pickup_datetime as timestamp) as dropoff_datetime,
    
    cast(Dispatching_base_num as string) as Dispatching_base_num,
    cast(Affiliated_base_number as string) as Affiliated_base_number,
    cast(SR_Flag as integer) as SR_Flag

from tripdata


-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}