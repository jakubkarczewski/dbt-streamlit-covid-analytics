{{ config(materialized="view") }}

with
    day_evaluation as (

        select
            date,
            country,
            case
                when new_active < 0
                then ':smile:'
                when new_active > 100
                then ':sob:'
                else ':rocket:'
            end day_evaluation
        from {{ ref("stg_prepared_source") }}


    )

select *
from day_evaluation
