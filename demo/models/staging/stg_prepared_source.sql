with
    stg_prepared_source as (select * from {{ source("source", "covid_data") }}),

    -- I know this is dumb since we have one record per date, but let's keep it for now
    final as (
        select
            date,
            country,
            sum(deaths) deaths,
            sum(confirmed) confirmed,
            sum(active) active,
            sum(new_deaths) new_deaths,
            sum(new_confirmed) new_confirmed,
            sum(new_active) new_active
        from stg_prepared_source
        group by date, country
        order by date
    )

select *
from final
