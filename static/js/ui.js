$(document).ready( function () {
    $('#start-picker').dateTimePicker({
        positionShift: { top: 20, left: 400},
    });
    $('#end-picker').dateTimePicker({
        positionShift: { top: 20, left: 500}
    });

    $('#select-form').submit( function(eventObj) {
        $("#select-form").append( "<input type='hidden' name='start-time' value='" + $("#start-time").val() + "'>");
        return true;
    });
})
