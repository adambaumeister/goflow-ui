$(document).ready( function () {

    var startTime = $.getUrlVar('start-time');
    var endTime = $.getUrlVar('end-time');

    if ( startTime == undefined ) {
        startTime = "1970-01-01 00:00"
    } else {
        startTime = decodeURIComponent($.getUrlVar('start-time'));
        // Forward populate input field if not empty
        $("#start-time").val(startTime)
    }

    if ( endTime == undefined ) {
        endTime = "now"
    } else {
        endTime = decodeURIComponent($.getUrlVar('end-time'));
        // Forward populate input field if not empty
        $("#end-time").val(endTime)
    }
    $('#start-picker').dateTimePicker({
        positionShift: { top: 20, left: 400},
        selectData: startTime
    });
    $('#end-picker').dateTimePicker({
        positionShift: { top: 20, left: 500},
        selectData: endTime
    });

    $('#select-form').submit( function(eventObj) {
        if ( $("#start-time").val() != '' ) {
            $("#select-form").append( "<input type='hidden' name='start-time' value='" + $("#start-time").val() + "'>");
        }
        if ( $("#end-time").val() != '' ) {
            $("#select-form").append( "<input type='hidden' name='end-time' value='" + $("#end-time").val() + "'>");
         }

        return true;
    });

    $('#flow-table').hpaging({
        "limit": 10
    });
})


$.extend({
  getUrlVars: function(){
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }
    return vars;
  },
  getUrlVar: function(name){
    return $.getUrlVars()[name];
  }
});