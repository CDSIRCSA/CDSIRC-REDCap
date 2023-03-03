select code, concat(code, " - ", description) as code_description
from icd_10_codes
limit 15000;