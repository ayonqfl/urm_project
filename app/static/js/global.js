$(document).ready(function() {
    applySelect2Theme();
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applySelect2Theme);

    // side-bar dropdown show, hide
    var currentPath = window.location.pathname;
    if (currentPath !== '/create_account' && currentPath !== '/user_list') {
        $('#userMenu').removeClass('show');
    }
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


function commonAutocomplete(element_id){
    element_id.on('input', function() {
        var query = $(this).val();
        if (query.length > 0) {
            $.get('api/autocompleteRoles', { query: query }, function(data) {
                var suggestions = $('#suggestionRoles');
                suggestions.empty(); // Clear any previous suggestions
                if (data.length > 0) {
                    data.forEach(function(item) {
                        suggestions.append('<li class="list-group-item">' + item + '</li>');
                    });
                    suggestions.show();
                } else {
                    suggestions.hide();
                }
            });
        } else {
            $('#suggestionRoles').hide();
        }
    });
    

    $(document).on('click', '#suggestionRoles li', function() {
        var selectedValue = $(this).text();
        element_id.val(selectedValue);
        $('#suggestionRoles').hide();
    });
}



function applySelect2Theme() {
    const darkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (darkMode) {
        $('.js-example-basic-multiple').select2({
            theme: 'dark',
        });
    } else {
        $('.js-example-basic-multiple').select2({
            theme: 'default',
        });
    }
}