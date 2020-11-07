$(document).ready(function (e) {
    var newtext = $('#apipage').text().replaceAll('_url_', location.hostname);
    $('#apipage').text(newtext)
})
