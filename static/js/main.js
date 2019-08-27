
$(document).ready(function () {
    if ((window.location.href === "http://localhost:5000/profiles")||(window.location.href === "http://localhost:5000/profiles?"))
        loggin_in();
    else {
         // removes the session so password will need to be entered again when you leave the page
        $.get('/close_session');

        // When page opens it checks to see if video and pictures are enabled or disabled. Displays the
        // appropriate message and also for few seconds displays the loader gif.
        $.ajax({
            url: '/get_feed_status',
            contentType: 'application/json;charset=UTF-8',
            type: 'GET',
            success: function (response) {
                // Displays the loader gif
                if (response === 'true') {
                     $('#imgHold').append('<img src="static/img/loading.gif" id="loadingGif">');
                     setTimeout(function () {
                        $('#loadingGif').remove();
                     }, 7000);
                } else if (response === 'false1'){
                    $("#msg_index").text("Pictures has been disabled. Check your settings.");
                } else if (response === 'false2'){
                    $("#msg_index").text("Video has been disabled. Check your settings.");
                }
            },
            error: function (error) {
                console.log(error);
            }
        })

    }//ends else

     // Sets the feed variable on the server side to 1 whenever profiles page is clicked.
     if(window.location.href === "http://localhost:5000/profiles"){
        const data = JSON.stringify({dataIn: '1'});
        ajaxCaller(data, false)
     }

});

function loggin_in() {

    // If there is no session it will prompt for a password.
    $.get("/is_session", function (data) {
        if (data === 'false')
            $("#loginModal").modal("show");
    })

    // This executes when submitting the login modal form.
    $("#loginFrm").on('submit', function(e){

        e.preventDefault();

        cred = { 'pwd': $("#inputPassword").val().trim() }
        const data = JSON.stringify(cred);

        // Verifies that the username and password are valid.
        $.ajax({
            url: '/verify_login',
            contentType: 'application/json;charset=UTF-8',
            data: data,
            type: 'POST',
            success: function (response) {
                console.log(response);
                if (response === 'login_success')
                    $("#loginModal").modal("hide");
                else
                    $("#loginModalMsg").text("Error login. Check your password.");
            },
            error: function (error) {
                $("#loginModalMsg").text(error.statusText);
                $("#inputPassword").val('')
            }
        });

    });

}

// Function to start the video feed on the main page. Triggered by the start button on the main page.
$("#btnStart").on('click', function () {
    const setVal = window.localStorage.getItem('optRadio');
    const data = JSON.stringify({dataIn: setVal});
    ajaxCaller(data, true)
});

// Function to stop the video feed on the main page. Triggered by the stop button on the main page.
$("#btnStop").on("click", function () {
    const data = JSON.stringify({'dataIn': '3'});
    ajaxCaller(data, false);
    $('#msg_index').text("Server stopped!");
});

// This executes when the profiles form is submitted.
$('#profileFrm').on('submit', function (e) {
    e.preventDefault();

    let ok2send = true;

    const data = {
        fob_id: $("#txtFobId").val().trim(),
        fname: $("#txtFname").val().trim(),
        lname: $("#txtLname").val().trim(),
        email: $("#txtEmail").val().trim(),
        phone: $("#txtPhone").val().trim(),
        comms: $("#inputState").find(":selected").text()
    };
    const data2 = JSON.stringify(data);

    if(data.comms === "EMail")
        if(data.email === ""){
            ok2send = false
            $("#profilesErrMsg").text("EMail cannot be left blank.");
         }
    if(data.comms === "SMS")
        if(data.phone === ""){
            ok2send = false;
            $("#profilesErrMsg").text("Phone number cannot be left blank.");
        }
    if(data.comms === "EMail/SMS")
        if((data.email === "")|(data.phone === "")){
            ok2send = false
            $("#profilesErrMsg").text("EMail or phone number cannot be left blank.");
        }

    // If validation passes the data gets sent to the server and saved to the database.
    if(ok2send){
        $.ajax({
            url: '/frmProfileSave',
            contentType: 'application/json;charset=UTF-8',
            data: data2,
            type: 'POST',
            success: function (response) {
                if (response === 'added')
                    location.reload();
                if (response === 'confirm')
                    $("#confirmModal").modal('show');
                if (response === 'login')
                    loggin_in();
            },
            error: function (error) {
                $("#profilesErrMsg").text(error.statusText);
            }
        });
    }
});

// Gets executed when the delete link on the profiles list gets clicked on.
$('.deleteLink').on('click', function () {

    const x = { id: $(this).attr('idRefDel') };

    $("#confirmDelModal").modal("show");

    $("#btnConfirmDelModalYes").on("click", function () {

        const y = JSON.stringify(x);

        //Sends info to server to delete the record.
        $.ajax({
            url: '/delete_profile',
            contentType: 'application/json;charset=UTF-8',
            data: y,
            type: 'POST',
            success: function (response) {
                if (response === 'deleted')
                    location.reload();
                if (response === 'login')
                    loggin_in();
            },
            error: function (error) {
                $("#profilesErrMsg").text(error.statusText);
                $("#confirmDelModal").modal("hide");
                console.log(error);
            }
        });

    });

});

// Gets executed when the update link on the profiles list gets clicked on. On click it retrieves
// the data from the database and puts it on the form for easier editing.
$(".updateLink").on('click', function () {

    const x = { id: $(this).attr('idRefUpdate') };
    const y = JSON.stringify(x);

    $.ajax({
        url: '/getOne_profile',
        contentType: 'application/json;charset=UTF-8',
        data: y,
        type: 'POST',
        success: function (response) {
            if (response) {
                response = JSON.parse(response);
                $("#txtFobId").val(response['fob_id']);
                $("#txtFname").val(response['fname']);
                $("#txtLname").val(response['lname']);
                $("#txtEmail").val(response['email']);
                $("#txtPhone").val(response['phone']);
                $("#inputState").val(response['comms']);
            }
        },
        error: function (error) {
            $("#profilesErrMsg").text(error.statusText);
            console.log(error);
        }
    });

});

// The confirmation modal comes up and if yes is clicked then it updates the database with the info on the form.
$("#btnConfirmModalYes").on('click', function () {

    const data = {
        fob_id: $("#txtFobId").val(),
        fname: $("#txtFname").val(),
        lname: $("#txtLname").val(),
        email: $("#txtEmail").val(),
        phone: $("#txtPhone").val(),
        comms: $("#inputState").find(":selected").text()
    };
    const data2 = JSON.stringify(data);

    $.ajax({
        url: '/update_profile',
        contentType: 'application/json;charset=UTF-8',
        data: data2,
        type: 'POST',
        success: function (response) {
            if (response === 'updated')
                location.reload();
        },
        error: function (error) {
            $("#profilesErrMsg").text(error.statusText);
        }
    });

});