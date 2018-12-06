$(document).ready( function () {
    $('#start-picker').dateTimePicker({
        positionShift: { top: 20, left: 400}
    });
    $('#end-picker').dateTimePicker({
        positionShift: { top: 20, left: 500}
    });

    $('#select-form').submit( function(eventObj) {
        $("#start-time").appendTo(this);
    });
})