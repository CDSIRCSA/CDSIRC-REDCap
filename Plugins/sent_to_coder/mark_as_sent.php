<?php
// Connect to REDCap (for authentication)
require_once "../../redcap_connect.php";
?>
<?php
// OPTIONAL: Display the project header
require_once APP_PATH_DOCROOT . 'ProjectGeneral/header.php';
?>

<div id="title">
    <h2>Mark cases as Sent to coder</h2><br>
    <p style="margin: auto; width: 500px;">By clicking the button below, all cases in the <strong>Cases for coding</strong> report will be marked as 'Sent to coder', except those cases still marked as 'To be de-identified'. Be sure that <i>all</i> cases marked as 'De-identified, to be sent' have indeed been sent to the coder before clicking this button.</p>
</div>
<div id="submitButton">
    <form method="post" action="<?php echo $_SERVER['PHP_SELF'] . '?pid=16'; ?>" onsubmit="return confirm('Are you sure?');">
        <input type="submit" name="mark_as_sent" value="Mark as sent">
    </form>
</div>
<?php
// Execute the action when the submit button is clicked
if(isset($_POST['mark_as_sent'])) 
{ 
    // Get data from the 'Cases for coding' report
    $report = REDCap::getReport('60');
    
    // Create a new array
    $data = array();
    
    // For each case (ignoring those yet to be de-identified)
    foreach($report as $case){
        if($case[43]['coding_status']==1){
            $data[$case[43]['case_number']][43]['coding_status'] = 2;
        }
    };
    
    // Save the data to REDCap
    $response = REDCap::saveData(16, 'array', $data);
    
    // Print the number of records updated
    echo '<p style="margin: auto; text-align: center;">';
    if($response['item_count']>0){
        print "Successfully updated coding status for {$response['item_count']} records.";
    }
    else {
        print "There are no records to update.";
    };
    echo '</p>';
    
};

?>
<!-- Import the CSS -->
<link rel="stylesheet" href="styles.css" type="text/css">
