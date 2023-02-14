<?php
// Connect to REDCap (for authentication)
require_once "../../redcap_connect.php";
?>

<!-- Import the CSS -->
<link rel="stylesheet" href="styles.css" type="text/css">

<!-- Case entry form (submitted to case_summary.php) -->
<div id="case_input" style="width: 50%; margin: auto; ">
    <p></p>
    
    
    <form action="case_summary.php" method="post" style="width: 100%; margin: auto;">
        
    <div style="width: 100%;">
        <h3 style="color: #800000; font-family: Verdana; width: 50%; display: inline-block;"><i>Enter case numbers</i></h3>
    </div>
    
    <input type="text" name="case1" placeholder="..."><br>
    <input type="text" name="case2" placeholder="..."><br>
    <input type="text" name="case3" placeholder="..."><br>
    <input type="text" name="case4" placeholder="..."><br>
    <input type="text" name="case5" placeholder="..."><br>
    <input type="text" name="case6" placeholder="..."><br>
    <input type="text" name="case7" placeholder="..."><br>
    <input type="text" name="case8" placeholder="..."><br>
    <input type="text" name="case9" placeholder="..."><br>
    <input type="text" name="case10" placeholder="..."><br>
    <input type="submit">
    </form>
    
</div>


