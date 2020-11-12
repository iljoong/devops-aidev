$(document).ready(function (e) {
    var newtext = $('#apipage').text().replaceAll('_url_', location.hostname);
    $('#apipage').text(newtext)

    // https://www.formget.com/ajax-image-upload-php/
    $("#uploadimage").on('submit', (function (e) {

        var api = "/api/score";

        $("#message").empty();
        $("#loading").show();

        e.preventDefault();

        $.ajax({
            url: api,          // Url to which the request is send
            type: "POST",             // Type of request to be send, called as method
            data: new FormData(this), // Data sent to server, a set of key/value pairs (i.e. form fields and values)
            contentType: false,       // The content type used when sending data to the server.
            cache: false,             // To unable request pages to be cached
            processData: false,        // To send DOMDocument or non processed data file it is set to false
        }).done(function (data)   // A function to be called if request succeeds
        {
            $("#loading").hide();
            //var d = JSON.parse(data);

            // show result
            $("#message").html("<br><b>Label:</b> " + data.label + ", <b>Confidence:</b> " + data.score);

        }).fail(function (data, status) {
            $("#loading").hide();
            alert("Internal Error!");
        });
    }));

    $("#file").change(function () {
        readURL(this);
    });

    $('.NO-CACHE').attr('src', function () { return $(this).attr('src') + "?a=" + Math.random() });
})

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#fruitimg').attr('src', e.target.result);
            $("#message").html("");
        };
        reader.readAsDataURL(input.files[0]);
    }
}