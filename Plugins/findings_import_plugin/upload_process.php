<?php
// Call the REDCap Connect file in the main "redcap" directory (for authentication, REDCap functions etc.)
require_once '../../redcap_connect.php';
?>

<?php
// Display the project header (i.e. the side menu)
require_once APP_PATH_DOCROOT . 'ProjectGeneral/header.php';
?>

<!-- Import the CSS -->
<link rel="stylesheet" href="styles.css" type="text/css">

<!-- Title and upload form -->
<div id="title">
<h2>Upload a list of coronial findings</h2>
</div>
<!-- File upload form -->
<div id="file_upload" style="text-align: center;">
<!-- The data encoding type, enctype, MUST be specified as below -->
<form enctype="multipart/form-data" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]).'?pid=16';?>" method="POST"> 
    <!-- MAX_FILE_SIZE must precede the file input field -->
    <input type="hidden" name="MAX_FILE_SIZE" value="30000" />
    <!-- Name of input element determines name in $_FILES array -->
    <input name="file" type="file" value="csv"/>
    <input type="submit" value="Upload file" name="Upload" />
</form>
</div>

<?php
// ----- PROCESS THE DATA -----
if($_SERVER["REQUEST_METHOD"] == "POST"){

    // Get BDM id and cause of death data from REDCap
    $redcap_data = REDCap::getData(16, 'array',null,array('case_number','bdm_id','cause_of_death'),null,null,false,false,false,'[bdm_id]!=""',true,false);
    // Create array with BDM IDs as keys and case numbers as values
    $bdm_ids = array();
    foreach($redcap_data as $case){
        $bdm_ids += [$case[43][bdm_id] => $case[43][case_number]];
    };

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
        $cod = $causes_of_death[$case["Registration Number"]]; //get the existing cause of death
        if($cod!=""){
            $cod = $cod."\r\n"; //append a new line if there is existing data
        };
        
        // Update the fields with data
        $processedData += [$bdm_ids[$case["Registration Number"]] => [43 => ["cause_of_death"=> $cod."FINDING (".date("d/m/Y")."): ".$case["Cause of Death 1A"]]]]; //start with the first field (which always exists)
        $processedData[$bdm_ids[$case["Registration Number"]]][43] += ["coronial_finding_made"=> "1"]; // update finding status
        $processedData[$bdm_ids[$case["Registration Number"]]][43] += ["coronial_finding"=> "FINDING (".date("d/m/Y")."): ".$case["Cause of Death 1A"]]; // place cause of death (finding) into finding field
        
        // Process the variable number of cause of death fields containing data
        foreach($case as $field => $value){
            if(in_array($field, $cod_fields)){
                if($value != ''){
                    $processedData[$bdm_ids[$case["Registration Number"]]][43]["cause_of_death"] = $processedData[$bdm_ids[$case["Registration Number"]]][43]["cause_of_death"] . "; " . $value;
                    $processedData[$bdm_ids[$case["Registration Number"]]][43]["coronial_finding"] = $processedData[$bdm_ids[$case["Registration Number"]]][43]["coronial_finding"] . "; " . $value;
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
    $n_records = count($processedData);
    // Print how many cases were updated
    if($n_records>1){
    ?>
        <div style="width: 500px; margin: auto;">
            <p style="text-align: center; padding-top: 15px;"><?php echo "Successfully saved {$n_records} findings!";?></p>
        </div>
    <?php
    }
    elseif($n_records==1){
    ?>
        <div style="width: 500px; margin: auto;">
            <p style="text-align: center; padding-top: 15px;"><?php echo "Successfully saved {$n_records} finding!";?></p>
        </div>
    <?php
    }
    // if no cases successfully processed
    else {
    ?>
        <div style="width: 500px; margin: auto;">
            <p style="text-align: center; padding-top: 15px;"><?php echo "No findings were saved.";?></p>
        </div>
    <?php
    }
    
}

?>


