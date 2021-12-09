<?php
/*
    Project-specific data entry form hook
*/

/**
 * Generate a dialog for entering two dates and write result to dtdiff input
 * 
 * Set:
 *  - $hookField - the text field to be populated with the calc result
 *  - $hookForm - the name of the form on which $hookField is found
 *  - $hookClickElementId - the id of the clickable element in the $hookField label or field note
 */

$hookField = "dtdiff";
$hookForm = "visit_data";
$hookClickElementId = "calcDtDiff";

if (isset($_GET['page']) && isset($_GET['id']) && $_GET['page'] == $hookForm) {
?>
<div id="dtdiff_dialog" title="Calculate date difference">
    <div style="margin:5px;">Enter your two dates:</div>
    <div style="margin:5px;"><span style="display:inline-block;width:50px">From: </span><input id="dtfrom" type="text"></div>
    <div style="margin:5px;"><span style="display:inline-block;width:50px">To: </span><input id="dtto" type="text"></div>
    <div style="margin:5px;">Difference: <span id="dtdiff_result"></span> days</div>
</div>
<script type='text/javascript'>
    function calcDtDiff() {
        var resultSpan = $('#dtdiff_result');
        resultSpan.text('');
        var dtFrom = $('#dtfrom').datepicker('getDate');
        var dtTo = $('#dtto').datepicker('getDate');
        if (dtFrom !== undefined && dtFrom !== null &&
            dtTo !== undefined && dtTo !== null) {
            var diff = (dtTo - dtFrom)/(1000*60*60*24);
            resultSpan.text(diff);
        }
    }
    $(document).ready(function() { 
        $('#dtfrom').datepicker({
            dateFormat: "dd-mm-yy",
            onSelect: calcDtDiff
        });
        $('#dtto').datepicker({
            dateFormat: "dd-mm-yy",
            onSelect: calcDtDiff
        });
        $('#dtdiff_dialog').dialog({
            autoOpen: false,
            modal: true,
            buttons: {
                Done: function() {
                    var calcResult = $('#dtdiff_result').html();
                    if (calcResult !== null) {
                        $('#<?php echo $hookField;?>-tr input').val(calcResult);
                        $( this ).dialog( "close" );
                    } else {
                        alert('No result calculated');
                    }
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            },
            open: function(event, ui) {
                $(":button:contains('Cancel')").focus();
            }
        });
        $('#<?php echo $hookClickElementId;?>').click(function() {
            $('#dtdiff_dialog').dialog('open');
        });
    });
</script>
<?php
}
