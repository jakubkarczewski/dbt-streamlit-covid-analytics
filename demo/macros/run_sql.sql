{% macro run_this_sql(country="Germany") %}

    {% set data_today  %}

        select  {{ dbt_date.today("Europe/Berlin") }}

    {% endset %}

    {% set sql_query  %}
         select to_char(date, 'YYYY') as _year,
                sum(new_deaths) deaths
        from {{ ref('stg_prepared_source') }}
        where country = {{"'"}}{{country}}{{"'"}}
        group by  _year
    {% endset  %}

{% if execute %}

{% set today = run_query(data_today).columns.values() %}
{{ log("Date ---- " ~ today, info=True) }}
{% set result = run_query(sql_query).columns.values() %}
{{ log("SQL results ---- " ~ result, info=True) }}

{% endif %}

{% endmacro %}
