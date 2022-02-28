// Nested country group dict - based on ABS classification
// A case's major (first digit) and minor (first 2 digits) country group codes with be extracted from its country code and used as keys to the dictionary; the group names are the values returned and added to the appropriate fields (and displayed on page)
var country_groups = {
    1: {name: 'Oceania and Antarctica',
        codes: {11: 'Australia (includes External Territories)', 12: 'New Zealand', 13: 'Melanesia', 14: 'Micronesia', 15: 'Polynesia (excludes Hawaii)', 16: 'Antarctica'}},
    2: {name: 'North-West Europe',
        codes: {21: 'United Kingdom, Channel Islands and Isle of Man', 22: 'Ireland', 23: 'Western Europe', 24: 'Northern Europe'}},
    3: {name: 'Southern and Eastern Europe',
        codes: {31: 'Southern Europe', 32: 'South Eastern Europe', 33: 'Eastern Europe'}},
    4: {name: 'North Africa and the Middle East',
        codes: {41: 'North Africa', 42: 'Middle East'}},
    5: {name: 'South-East Asia',
        codes: {51: 'Mainland South-East Asia', 52: 'Maritime South-East Asia'}},
    6: {name: 'North-East Asia',
    codes: {61: 'Chinese Asia (includes Mongolia)', 62: 'Japan and the Koreas'}},
    7: {name: 'Southern and Central Asia',
        codes: {71: 'Southern Asia', 72: 'Central Asia'}},
    8: {name: 'Americas',
        codes: {81: 'Northern America', 82: 'South America', 83: 'Central America', 84: 'Caribbean'}},
    9: {name: 'Sub-Saharan Africa',
        codes: {91: 'Central and West Africa', 92: 'Southern and East Africa'}}}
;

//
var country = 1101;
var child_major_group = String(country).substring(0,1);
var child_minor_group = String(country).substring(0,2);
console.log(child_minor_group)
console.log(country_groups[child_major_group].name)
console.log(country_groups[child_major_group].codes[child_minor_group])

