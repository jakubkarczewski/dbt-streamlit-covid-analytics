-- this works but is completely wrong
{{ config(materialized="incremental", unique_key=["country", "month_year"]) }}

with
    stg_deaths_per_month as (
        select country, to_char(date, 'YYYY-MM') as month_year, sum(new_deaths) deaths


        from {{ ref("stg_prepared_source") }} as ps

        {% if is_incremental() %}

        -- this filter will only be applied on an incremental run
        where ps.date >= (select max(date) from {{ ref("stg_prepared_source") }})

        {% endif %}

        group by country, month_year
    )

select *
from stg_deaths_per_month
