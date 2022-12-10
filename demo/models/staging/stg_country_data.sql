with
    stg_country_data as (

        select country, slug, {{ '"' }}iso2{{ '"' }} as code, population
        from {{ source("source", "countries") }}
        where country is not null
    )

select *
from stg_country_data
