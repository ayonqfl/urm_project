function show_error_message(msg){
    $('#toast_msg').text(msg);
    tata.error('', $('#toast_msg').text(), {
        position: 'tr',
        duration: 2000
    })
}

function show_success_message(msg){
    $('#toast_msg').text(msg);
    tata.success('', $('#toast_msg').text(), {
        position: 'tr',
        duration: 2000,
    })
}
