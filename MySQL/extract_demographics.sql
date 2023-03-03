select CAST(a.record AS UNSIGNED) as "case_number", a.value AS "given_names", b.value as "surname", c.value as "dob",
	d.value as "mother_givenname", e.value as "mother_surname", f.value as "mother_dob",
    g.value as "father_givenname", h.value as "father_surname", i.value as "father_dob"
from redcap_data a
left join redcap_data b on a.record = b.record
left join redcap_data c on a.record = c.record
left join redcap_data d on a.record = d.record
left join redcap_data e on a.record = e.record
left join redcap_data f on a.record = f.record
left join redcap_data g on a.record = g.record
left join redcap_data h on a.record = h.record
left join redcap_data i on a.record = i.record

where a.field_name = "given_names" and b.field_name = "surname" and c.field_name = "dob"
