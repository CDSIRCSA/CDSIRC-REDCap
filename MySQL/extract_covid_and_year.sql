select a.record, a.value AS "impacts_of_covid_19", b.value AS "year_of_death"	
from redcap_data a
left join redcap_data b on a.record = b.record
where a.field_name = "impacts_of_covid_19" and b.field_name = "year_of_death" and b.value > 2020