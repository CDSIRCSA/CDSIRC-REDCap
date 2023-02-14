<?php
// Connect to REDCap (for authentication and access to developer methods)
require_once "../../redcap_connect.php";
?>

<!-- Import the CSS -->
<link rel="stylesheet" href="styles.css" type="text/css">

<?php
// Get the data (from case_form.php) and save as an array
$cases = array();
foreach(array_slice($_POST, 1) as $key => $value){ //slice out the first value (the agenda_paper checkbox)
    if($value){
        array_push($cases, $value);
    };
};

// Loop through cases
foreach($cases as $case){
    // get their data
    $data = REDCap::getData(16, 'array', $case, array('case_number','given_names','surname','mother_givenname','mother_surname'));
    $data = $age_data[$case][43];
    
    ?>
    <!-- display their data -->
    <div id="main-display">
        <?php
        // if the agenda paper 3.1 checkbox is checked, render the label
        if($_POST['agenda_check']=="1"){
            ?>
            <div style="padding-bottom: 30px;">
                <p><strong id="agenda_paper">Agenda paper 3.1</strong></p>
                <br>
            </div>
            <?php
        };
        ?>
        
        <h3 style="color: #800000">Case <?php echo $case?></h3>
        <table style="page-break-after: always;">
            <tbody>
                <colgroup>
                    <col width="40%">
                    <col width="60%">
                </colgroup>
                
            </tbody>
        </table>
    </div>

<?php   
};
?>
