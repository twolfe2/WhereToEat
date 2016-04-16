$(document).ready(function() {



    function show() {
    $('#loading').hide();
    $('#container').fadeIn();
};

setTimeout(show, 5000);


    $('#new-city').hide();

    $('form').on('submit', function() {

        userInput = $('input[name="city"]').val();
        console.log(userInput)

        $.ajax({
            type: "POST",
            url: "/",
            data: {'city': userInput},
            success: function(results) {

                if(results) {
                    $('#submit').hide();
                    $('input').hide();
                    $('#new-city').show();
                    console.log(results)
                    console.log(results.name)
                    $('#results').html('<a href="'+results.url+'">'+results.name+
              '</a><br><img src="'+results.image+'" >')
                } else {
                    $('#results').html('Error, please try again.')
                }
            },
            error: function(error) {
                console.log(error)
            }




        });
    });

    $('#new-city').on('click', function(){
        $('input').val('').show();
        $('#new-city').hide();
        $('#results').html('');
        $('#submit').show();
    });


});