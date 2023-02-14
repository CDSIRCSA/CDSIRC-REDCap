<?php
// Connect to REDCap (for authentication)
require_once "../../redcap_connect.php";
?>

<!-- Import the CSS -->
<link rel="stylesheet" href="styles.css" type="text/css">

<!-- Case entry form (submitted to case_summary.php) -->
<div style="width: 50%; margin: auto; ">
    <h1>Case linking plugin</h1>
    <p></p>
    
    
    <form action="case_link_process.php" method="post" style="width: 100%; margin: auto;">
        
        <input type="submit" class="button" name="run-button" value="Run">
    
    </form>
    
</div>