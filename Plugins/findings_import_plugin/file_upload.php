<?php
// Call the REDCap Connect file in the main "redcap" directory
require_once '../../redcap_connect.php';
?>

<?php
// OPTIONAL: Display the project header
require_once APP_PATH_DOCROOT . 'ProjectGeneral/header.php';
?>

<!-- Import the CSS -->
<link rel="stylesheet" href="styles.css" type="text/css">

<div id="title">
<h2>Upload a list of Coronial findings</h2>
</div>

<!-- File upload -->
<div id="file_upload" style="text-align: center;">
<!-- The data encoding type, enctype, MUST be specified as below -->
<form enctype="multipart/form-data" action="process_file.php" method="POST">
    <!-- MAX_FILE_SIZE must precede the file input field -->
    <input type="hidden" name="MAX_FILE_SIZE" value="30000" />
    <!-- Name of input element determines name in $_FILES array -->
    <input name="file" type="file" value="csv"/>
    <input type="submit" value="Upload file" name="Upload" />
</form>
</div>

