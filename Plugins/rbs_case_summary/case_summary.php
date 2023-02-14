<?php
// Connect to REDCap (for authentication and access to developer methods)
require_once "../../redcap_connect.php";
?>

<!-- Import the CSS -->
<link rel="stylesheet" href="styles.css" type="text/css">

<?php
// Get the data (from case_form.php) and save as an array
$cases = array();
foreach($_POST as $key => $value){ 
    if($value){
        array_push($cases, $value);
    };
};

// Loop through cases
foreach($cases as $case){
    // get their data
    $age_data = REDCap::getData(16, 'array', $case, array('age_group','age_days','age_months','age_years','gestation','birthweight'));
    $age_data = $age_data[$case][43];
	$screening_data = json_decode(REDCap::getData(16, 'json', $case, array('given_names','surname','dod','sex','cultural_background','cald','seifa_disadvantage','cause_of_death','circumstances_of_harm','cp_summary','cdr_status_entries','screening_outcomes','sig_actions','sig_updates','manner_of_death','mod_info','country_of_birth','mother_country_of_birth','father_country_of_birth'), null, null, false, false, false, null, true, null), true)[0];//use json here so labels can be exported, then decode and extract the inner array

    $age = "";
    // compute which age value to use
    if ($age_data['age_group'] == '< 28 days'){
        $age = $age_data['age_days']. " days";
    }
    else if ($age_data['age_group'] == '1 to 11 months'){
        $age = $age_data['age_months']. " months";
    }
    else {
        $age = $age_data['age_years']. " years"; 
    };
    
    if($screening_data['cp_summary']==""){
        $screening_data['cp_summary'] = "Nil";
    };
    
    ?>
    <!-- display their data -->
    <div id="main-display">
        
        <h3 style="color: #800000">Case <?php echo $case?></h3>
        <table>
            <tbody>
                <colgroup>
                    <col width="40%">
                    <col width="60%">
                </colgroup>
                <tr>
                    <td colspan="2"><p><strong>Name: &nbsp;&nbsp;&nbsp;</strong><?php echo $screening_data['given_names'] .' '. $screening_data['surname']?></p></td>
                </tr>
                <tr>
                    <td colspan="1"><p><strong>Age: &nbsp;&nbsp;&nbsp;</strong><?php echo $age ?></p></td>
                    <td colspan="1"><p><strong>Date of death: &nbsp;&nbsp;&nbsp;</strong><?php echo date_format(date_create($screening_data['dod']), "d/m/Y");?></p></td>
                </tr>
                <?php 
                if ($age_data['age_months'] <= 12){?>
                    <tr>
                        <td><p><strong>Gestation: &nbsp;&nbsp;&nbsp;</strong><?php echo $age_data['gestation']?></p></td>
                        <td><p><strong>Birthweight: &nbsp;&nbsp;&nbsp;</strong><?php echo $age_data['birthweight']?></p></td>
                    </tr>
                <?php
                };
                ?>
                <tr>
                    <td colspan="1"></p><p><strong>Sex: &nbsp;&nbsp;&nbsp;</strong><?php echo $screening_data['sex'] ?></p></td>
                    <td colspan="1"><p><strong>CALD background: &nbsp;&nbsp;&nbsp;</strong><?php echo $screening_data['cald'] ?></p></td>
                </tr>
                <tr>
                    <td colspan="1"><p><strong>SEIFA: &nbsp;&nbsp;&nbsp;</strong><?php echo $screening_data['seifa_disadvantage']?></p></td>
                    <td colspan="1"><p><strong>Cultural background: &nbsp;&nbsp;&nbsp;</strong><?php echo $screening_data['cultural_background'] ?></p></td>
                </tr>
                <?php 
                if ($screening_data['cald'] == 'Yes'){?>
                    <tr>
                        <td colspan="2"><p><strong>Country of birth: &nbsp;&nbsp;&nbsp;</strong><?php echo $screening_data['country_of_birth']?></p></td>
                    </tr>
                    <tr>
                        <td colspan="2"><p><strong>Mother's country of birth: &nbsp;&nbsp;&nbsp;</strong><?php echo $screening_data['mother_country_of_birth']?></p></td>
                    </tr>
                    <tr>
                        <td colspan="2"><p><strong>Father's country of birth: &nbsp;&nbsp;&nbsp;</strong><?php echo $screening_data['father_country_of_birth']?></p></td>
                    </tr>
                <?php
                };
                ?>
                <tr>
                    <td colspan="2"><p><strong>Manner of death: &nbsp;&nbsp;&nbsp;</strong><?php echo $screening_data['manner_of_death']?></p></td>
                </tr>
                <tr>
                    <td colspan="2"><p><strong>Manner of death information: &nbsp;&nbsp;&nbsp;</strong><?php echo $screening_data['mod_info']?></p></td>
                </tr>
                <tr>
                    <td class="pad-bottom" colspan="2" style="padding-top: 20px;"><p><strong>Cause of death:</strong><br><?php echo $screening_data['cause_of_death']?></p></td>
                </tr>
                <tr>
                    <td class="pad-bottom" colspan="2"><p><strong>Circumstances of harm:</strong><br><?php echo $screening_data['circumstances_of_harm']?></p></td>
                </tr>
                <tr>
                    <td  class="pad-bottom" colspan="2"><p><strong>Child protection summary:</strong><br><?php echo $screening_data['cp_summary']?></p></td>
                </tr>
                <?php 
                if ($screening_data['cdr_status_entries'] != ''){?>
                    <tr>
                        <td class="pad-bottom" colspan="2"><p><strong>CDR status entries:</strong><br><?php echo $screening_data['cdr_status_entries']?></p></td>
                    </tr>
                <?php
                };
                ?>
                <tr>
                    <td class="pad-bottom" colspan="2"><p><strong>Proposed SIG actions: </strong><br><?php echo $screening_data['sig_actions']?></p></td>
                </tr>
                <tr>
                    <td class="pad-bottom" colspan="2"><p><strong>SIG updates:</strong><br><?php echo $screening_data['sig_updates']?></p></td>
                </tr>
            </tbody>
        </table>
    </div>

<?php   
};
?>

