<?php
// Call the REDCap Connect file in the main "redcap" directory
require_once '../../redcap_connect.php';
?>

<?php
// Load the ChromePhp extension for debugging
require_once 'ChromePhp.php';
?>

<?php
// Get BDM id and cause of death data from REDCap
$redcap_data = REDCap::getData(16, 'array',null,array('case_number','bdm_id','cause_of_death'),null,null,false,false,false,'[bdm_id]!=""',true,false);
// Create array with BDM IDs as keys and case numbers as values
$bdm_ids = array();
foreach($redcap_data as $case){
    $bdm_ids += [$case[43][bdm_id] => $case[43][case_number]];
};
//ChromePhp::log($bdm_ids);

// Create array with BDM IDs as keys and cause of death as values
$causes_of_death = array();
foreach($redcap_data as $case){
    $causes_of_death += [$case[43][bdm_id] => $case[43][cause_of_death]];
};
//ChromePhp::log($causes_of_death);
?>

<?php
// Read the uploaded csv file into an array
$csvFile = $_FILES["file"]["tmp_name"];
//ChromePhp::log($csvFile);

$rows = array_map('str_getcsv', file($csvFile));
array_pop($rows); // delete the last row which contains only a row count
$header = array_shift($rows);
$csv = array();
foreach($rows as $row){
    $csv[] = array_combine($header, $row);
};
?>

<?php
// Process the cause of death fields
$processedData = array(); //create new array to store processed data
$cod_fields = array("Cause of Death 1B","Cause of Death 1C","Cause of Death 1D","Cause of Death 1E","Cause of Death 2A","Cause of Death 2B","Cause of Death 2C","Cause of Death 2D","Cause of Death 2E","Cause of Death 2F");

foreach($csv as $case){
    $cod = $causes_of_death[$case["Registration Number"]];
    if($cod!=""){
        $cod = $cod."\r\n";
    };
    $processedData += [$bdm_ids[$case["Registration Number"]] => [43 => ["cause_of_death"=> $cod."FINDING (".date("d/m/Y")."): ".$case["Cause of Death 1A"]]]];
    //ChromePhp::log($processedData);
    
    foreach($case as $field => $value){
        if(in_array($field, $cod_fields)){
            if($value != ''){
                $processedData[$bdm_ids[$case["Registration Number"]]][43]["cause_of_death"] = $processedData[$bdm_ids[$case["Registration Number"]]][43]["cause_of_death"] . "; " . $value;
            }
        }
    }
}

// Check the output
/*
echo '<pre>';
print_r($processedData);
echo '</pre>';
*/

// Save the data to REDCap
$response = REDCap::saveData(16, 'array', $processedData);

// Print the number of records saved
echo '<pre>';
print "Successfully saved {$response['item_count']} records!";
echo '</pre>';
?>


