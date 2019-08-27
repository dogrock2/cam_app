
// Checks if the video or picture radio button is selected. Sends the setting to the database whenever the radio
// buttons is changed so the server knows if it needs to send a pic or record/send the video clip. The selected
// value is also stored in local storage so it can keep setting after changing the page.
// Note: The variable at the server side is called feed. 1 = pictures and 2 = videos


let setVal = window.localStorage.getItem('optRadio');
if (!setVal){
    setVal = '1'
    window.localStorage.setItem('optRadio', '1');
}

$(document).ready(function () {

            if(setVal === '1')
                 $('#optradio1').attr('checked', true);
            if(setVal === '2')
                 $('#optradio2').attr('checked', true);

            const data = JSON.stringify({dataIn: setVal});
            ajaxCaller(data, false)

});

    const dataSet = { dataIn: '1' }
    $('input[name=optradio]').change(function(){
        const x = $('input[name=optradio]:checked').attr("aVal");
        window.localStorage.setItem('optRadio', x);
        dataSet.dataIn = x
        const data2 = JSON.stringify(dataSet);
        ajaxCaller(data2, true)

    })



function ajaxCaller(data2, relo){

     $.ajax({
            url: '/set_global_feed',
            contentType: 'application/json;charset=UTF-8',
            data: data2,
            type: 'POST',
            success: function (response) {
                if (response) {
                    console.log(response)
                }
            },
            error: function (error) {
                console.log(error);
            }
        }).then(function(){
        if (relo)
//            location.reload();
            window.location.href = "http://localhost:5000";
        });

}


