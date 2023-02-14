<?php
$processedData = array();

$processedData += [0 => [43 => ["cause_of_death"=> "test"]]];
$processedData[0][43] += ["coronial_finding_made"=> "1"];

echo '<pre>';
print_r($processedData);
echo '</pre>';

echo count($processedData);
echo '<br>';
echo count($processedData[0]);
?>
