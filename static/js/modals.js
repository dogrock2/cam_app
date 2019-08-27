
//Disables or enables textboxes when checkbox is clicked
$("#camChk").on('click', function(){
    setTextboxState();
});
$("#vidChk").on('click', function(){
    setTextboxState();
});

function setTextboxState(){

    if($("#vidChk").is(':checked')){
        $("#inputVidRes").removeAttr("disabled");
       // $("#inputVidTime").removeAttr("disabled");
        $("#inputVidLength").removeAttr("disabled");
    } else {
        $("#inputVidRes").attr("disabled", "disabled");
        $("#inputVidTime").attr("disabled", "disabled");
        $("#inputVidLength").attr("disabled", "disabled");
    }

    if($("#camChk").is(':checked')){
        //$("#inputPicRes").removeAttr("disabled");
        //$("#inputPicTime").removeAttr("disabled");
    } else {
        $("#inputPicRes").attr("disabled", "disabled");
        $("#inputPicTime").attr("disabled", "disabled");
    }

}

//These 3 functions are for setting the plus and minus icons on the
//settings modal. This is for show only wont affect functionality.
$('#picSettingsLink').on('click', function () {    
    if ($('#collapseOne').hasClass('show'))
        $('#picSettingsIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
    else
        $('#picSettingsIcon').html('<i class="fa fa-minus" aria-hidden="true"></i>');

    $('#videoSettingsIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
    $('#pwdMngIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
    $('#adminProfileIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
});
$('#videoSettingsLink').on('click', function () {    
    if ($('#collapseTwo').hasClass('show'))
        $('#videoSettingsIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
    else
        $('#videoSettingsIcon').html('<i class="fa fa-minus" aria-hidden="true"></i>');

    $('#pwdMngIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
    $('#picSettingsIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
    $('#adminProfileIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
});
$('#pwdMngLink').on('click', function () {    
    if ($('#collapseThree').hasClass('show'))
        $('#pwdMngIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
    else
        $('#pwdMngIcon').html('<i class="fa fa-minus" aria-hidden="true"></i>');

    $('#picSettingsIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
    $('#videoSettingsIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
    $('#adminProfileIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
});


$('#adminProfileLink').on('click', function () {    
    if ($('#collapseFour').hasClass('show'))
        $('#adminProfileIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
    else
        $('#adminProfileIcon').html('<i class="fa fa-minus" aria-hidden="true"></i>');

    $('#picSettingsIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
    $('#videoSettingsIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
    $('#pwdMngIcon').html('<i class="fa fa-plus" aria-hidden="true"></i>');
});