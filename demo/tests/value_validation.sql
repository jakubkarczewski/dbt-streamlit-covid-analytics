select *
from {{ ref('stg_prepared_source')}}
where new_active > active
