
// Whwn the settings modal closes it ends the session so every time its open the password will need to be entered.
$("#settingsModal").on("hidden.bs.modal", function () {
    $("#inputPassword").val("")
    $.get('/close_session');
});

// Function to update the admin password. It checks with the database and verifies that the old password matches
// what was entered.
$("#btnSavePwd").on('click', function(){
        original_pwd = $("#txtOriginalPwd").val().trim();
        new_pwd = $("#txtNewPwd").val().trim();
        confirm_pwd = $("#txtConfirmPwd").val().trim();

        if(new_pwd === confirm_pwd){
            const pwd_obj = {
                pwd : original_pwd,
                pwd2 : new_pwd
            }
            const data = JSON.stringify(pwd_obj);
            $.ajax({
                url: '/chng_pwd',
                contentType: 'application/json;charset=UTF-8',
                data: data,
                type: 'POST',
                success: function(response) {
                    if(response === 'Password changed'){
                       $("#modalSettingsMsg").text("Admin password successfully updated!");
                       $("#txtOriginalPwd").val("");
                       $("#txtNewPwd").val("");
                       $("#txtConfirmPwd").val("");
                    } else if(response === 'Not logged in.')
                        $("#modalSettingsMsg").text(response);
                    else if(response === "mismatch")
                        $("#modalSettingsMsg").text("Original password mismatch. Check your spelling.");
                },
                error: function(error) {
                    $("#modalSettingsMsg").text(error.statusText);
                }
            });

        } else
            $("#modalSettingsMsg").text("Confirm password must match.");
});

// When the settings link in the navbar gets clicked it first asks for password to log in. If login is successful then
// it gets the data from the database and puts the data in the settings modal's form.
$("#settingsBtn").on("click", function(){

    $("#loginModal").modal("show");

    $("#loginFrm").on('submit', function(e){

        e.preventDefault();

        cred = { 'pwd': $("#inputPassword").val().trim() }
        const data = JSON.stringify(cred);

        $.ajax({
        url: '/verify_login',
        contentType: 'application/json;charset=UTF-8',
        data: data,
        type: 'POST',
        success: function(response) {
            if(response === 'login_success'){
                $.get('/settings', function(data){
                    $("#loginModal").modal("hide");
                    if(data !== "None"){
                        data = JSON.parse(data);
                        $('#settingsModal').modal('show');
                        if(data['picEnable'])
                            $('#camChk').prop('checked', true)
                        else
                            $('#camChk').prop('checked', false)
                        $('#inputPicRes').val(data['picRes']);
                        $('#inputPicTime').val(data['picTime']);


                        if(data['videoEnable'])
                            $('#vidChk').prop('checked', true)
                        else
                            $('#vidChk').prop('checked', false)
                        $('#inputVidRes').val(data['videoRes']);
                        $('#inputVidTime').val(data['videoTime']);
                        $('#inputVidLength').val(data['videoLength']);


                        $('#inputAdminEmail').val(data['email']);
                        $('#inputAdminPhone').val(data['phone']);
                        $('#inputAdminRFID').val(data['rfidLocation']);
                        $('#inputAdminAPIKey').val(data['apiKey']);
                        $('#inputTokenAPIKey').val(data['tokenKey']);
                        $('#inputTwilioPhone').val(data['twPhone']);
                    }

            }).done(function(){
                setTextboxState();
            }); }//ends first if
            if(response === 'login_fail'){
                $("#loginModalMsg").text("Incorrect password.");
                $("#inputPassword").val("")
            }
        },
        error: function(error) {
            $("#modalSettingsMsg").text(error.statusText);
        }
    });

    });
});

// Updates the picture settings in the database.
$("#btnSavePic").on('click', function(){

    inputPicRes = $('#inputPicRes').val().trim();
    inputPicTime = $('#inputPicTime').val().trim();
    if($('#camChk').is(":checked"))
        picChkBox = true
    else
        picChkBox = false

    picObj = {
        picRes : inputPicRes,
        picTime : inputPicTime,
        picChk : picChkBox
    };
    const data = JSON.stringify(picObj);

      $.ajax({
        url: '/updatePic',
        contentType: 'application/json;charset=UTF-8',
        data: data,
        type: 'POST',
        success: function(response) {
            if(response === 'updated')
               $("#modalSettingsMsg").text("Picture settings successfully updated!")
        },
        error: function(error) {
            $("#profilesErrMsg").text(error.statusText);
        }
    });

});

// Updates the video settings in the database.
$("#btnSaveVid").on('click', function(){

    inputVidRes = $('#inputVidRes').val().trim();
    inputVidTime = $('#inputVidTime').val().trim();
    inputVidLength = $('#inputVidLength').val().trim();
    if($('#vidChk').is(":checked"))
        vidChkBox = true
    else
        vidChkBox = false

    vidObj = {
        vidRes : inputVidRes,
        vidTime : inputVidTime,
        vidChk: vidChkBox,
        vidLength: inputVidLength
    };

    const data = JSON.stringify(vidObj);

      $.ajax({
        url: '/updateVid',
        contentType: 'application/json;charset=UTF-8',
        data: data,
        type: 'POST',
        success: function(response) {
            if(response === 'updated')
               $("#modalSettingsMsg").text("Video settings successfully updated!")
        },
        error: function(error) {
            $("#profilesErrMsg").text(error.statusText);
        }
    });

});


// Updates the Admin settings in the database.
$("#btnSaveProfile").on('click', function(){

    inputAdminEmail = $('#inputAdminEmail').val().trim();
    inputAdminPhone = $('#inputAdminPhone').val().trim();
    inputAdminRFID = $('#inputAdminRFID').val().trim();
    inputAdminAPIKey = $('#inputAdminAPIKey').val().trim();
    inputAdminToken = $('#inputTokenAPIKey').val().trim();
    inputTwilioPhone = $('#inputTwilioPhone').val().trim();

    adminObj = {
        adminEmail : inputAdminEmail,
        adminPhone : inputAdminPhone,
        adminApiKey: inputAdminAPIKey,
        adminToken: inputAdminToken,
        adminRFID: inputAdminRFID,
        twilioPhone: inputTwilioPhone
    };

    const data = JSON.stringify(adminObj);

      $.ajax({
        url: '/updateAdmin',
        contentType: 'application/json;charset=UTF-8',
        data: data,
        type: 'POST',
        success: function(response) {
            if(response === 'updated')
               $("#modalSettingsMsg").text("Admin settings successfully updated!");
        },
        error: function(error) {
            $("#profilesErrMsg").text(error.statusText);
        }
    });

});