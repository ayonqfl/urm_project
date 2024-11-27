$(document).ready(function() {
    // $('#filter_role_name').select2({
    //     theme: 'bootstrap-5',
    //     placeholder: "Enter Role Name",
    //     allowClear: true
    // });
});


function show_error_message(msg){
    $('#toast_msg').text(msg);
    tata.error('', $('#toast_msg').text(), {
        position: 'tr',
        duration: 5000
    })
}

function show_success_message(msg){
    $('#toast_msg').text(msg);
    tata.success('', $('#toast_msg').text(), {
        position: 'tr',
        duration: 5000,
    })
}
