$(document).ready(function () {


    function show() {

        $('.container').fadeIn();
    };


    setTimeout(show, 50000);

    $('#results').hide();

//var options = {
//	data: ["blue", "green", "pink", "red", "yellow"]
//};
//
//$("#basics").easyAutocomplete(options);
//
    $('#new-city').hide();

    $(function () {
        3
        $("#geocomplete").geocomplete()
        4
    });


    $('form').on('submit', function () {

        userInput = $('input[name="city"]').val();
        console.log(userInput)

        $.ajax({
            type: "POST",
            url: "/",
            data: {'city': userInput},
            success: function (results) {

                if (results) {
                    $('#submit').hide();
                    $('input').hide();
                    $('#new-city').show();
                    console.log(results)
                    console.log(results.name)
                    //$('#restInfo').text(results.info)
                    $('#restName').text(results.name);
                    $('#restImg').attr("src", results.image);
                    $('#restPhone').hide();
                    //don't show phone icon if no phone number
                    if (results.phone !== "false") {
                        $('#restPhone').attr("href", "tel:" + results.phone);
                        $('#restPhone').show();
                    }
                    $('#restLink').attr("href", results.url);

                    //      $('#results').html('<a href="'+results.url+'">'+results.name+
                    //'</a><br><img src="'+results.image+'" >')
                    $('#results').show();

                } else {

                    $('#results').html('Error, please try again.')
                    $('#results').show();
                }
            },
            error: function (error) {
                console.log(error)
            }


        });
    });

    $('#new-city').on('click', function () {
        $('input').val('').show();
        $('#new-city').hide();
        $('#results').hide();
        $('#submit').show();
    });


});