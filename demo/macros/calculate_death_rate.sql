{% macro calc_death_rate(n=4) %}

(dpm.deaths / cd.population) * {{ 10**n }}

{% endmacro %}
