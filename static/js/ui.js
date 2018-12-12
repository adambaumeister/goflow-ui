$(document).ready( function () {

    var startTime = $.getUrlVar('start-time');
    var endTime = $.getUrlVar('end-time');
    var search = $.getUrlVar('search');

    //
    // Forward populate input fields with get params
    //
    if ( startTime == undefined ) {
        startTime = "now";
    } else {
        startTime = decodeURIComponent($.getUrlVar('start-time'));
        // Forward populate input field if not empty
        $("#start-time").val(startTime);
    }

    if ( endTime == undefined ) {
        endTime = "now"
    } else {
        endTime = decodeURIComponent($.getUrlVar('end-time'));
        // Forward populate input field if not empty
        $("#end-time").val(endTime)
    }
    if ( search != undefined ) {
        var s = decodeURIComponent(search);
        res = s.replace(/\+/g, " ");
        $("#search").val(res);
    }

    if ( endTime == startTime) {
        $(".time-buttons").hide();
        $(".time-shroud").show();
    }

    $(".time-shroud").click(function() {
        $(".time-shroud").hide()
        $(".time-buttons").show()
    });

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
        if ( $("#search").val() != '' ) {
            $("#select-form").append( "<input type='hidden' name='search' value='" + $("#search").val() + "'>");
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