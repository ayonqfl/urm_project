
$(document).ready(function () {
    $('#ac_role_name').select2({
        placeholder: 'Select Roles',
        allowClear: true,
        ajax: {
            url: '/api/userRoles',
            type: 'GET',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    query: params.term || '',
                    limit: 10
                };
            },
            processResults: function (data) {
                return {
                    results: data.map(function (item) {
                        return { id: item, text: item };
                    })
                };
            },
            cache: true
        },
        minimumInputLength: 0,
        dropdownCssClass: "select2-dropdown",
    });

    $('#ac_role_name').on('select2:open', function () {
        const $select = $(this);
        if (!$select.data('loaded')) {
            $.ajax({
                url: '/api/userRoles',
                type: 'GET',
                dataType: 'json',
                data: { limit: 10 },
                success: function (data) {
                    data.forEach(function (item) {
                        const option = new Option(item, item, false, false);
                        $select.append(option);
                    });
                    $select.trigger('change');
                    $select.data('loaded', true);
                }
            });
        }
    });

    get_api_user_list();
});


function create_api_user(){
    const params = {
        username: $('#user_username').val(),
        user_type: $('#userType').val(),
        password: $('#user_password').val(),
        confirmPassword: $('#user_confirmPassword').val(),
        roles: $('#ac_role_name').val() || [],
        email: $('#user_email').val(),
        phone: $('#user_phone').val(),
        details: $('#user_details').val(),
    }
    console.log(params);

    $.ajax({
        url: 'api/create_api_user',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(params),
        success: function (success) {
            $('#user_username').val('');
            $('#userType').val('');
            $('#user_password').val(''),
            $('#user_confirmPassword').val('');
            $('#ac_role_name').val(null).trigger('change');
            $('#user_email').val('');
            $('#user_phone').val('');
            $('#user_details').val('');
            show_success_message(success.success);
        },
        error: function (error) {
            show_error_message(error.responseJSON.error);
        }
    });
}


function get_api_user_list() {
    const params = {
        username: $('#filter_username').val(),
        user_type: $('#filter_user_type').val()
    }
    $.get('api/api_user_list', params)
        .done(function (data) {
            $('#tbody_api_user_list').empty();
            // console.log(data);
            if (data.length > 0) {
                data.forEach(function (item) {
                    const roles = item.roles.map(role => `
                        <span class="border border-secondary rounded py-0.5 px-2 m-1 text-sm">${role}</span>
                    `).join('');

                    const row = `
                    <tr>
                        <td>${item.username}</td>
                        <td><span class="text-warning">${item.type}</span></td>
                        <td>${roles || '<span class="text-muted">No Roles</span>'}</td>
                        <td>${item.created_at}</td>
                        <td class="text-end">
                            <button type="button" class="btn btn-sm btn-primary"><i class="fas fa-edit text-sm"></i></button>
                            <button type="button" class="btn btn-sm btn-danger" onclick="deleteApiUser('${item.id}')"><i class="fas fa-trash-alt text-sm"></i></button>
                        </td>
                    </tr>
                    `;
                    $('#tbody_api_user_list').append(row);
                });
            } else {
                const noDataRow = `
                    <tr>
                        <td colspan="5" class="text-center my-2">No data available</td>
                    </tr>
                `;
                $('#tbody_api_user_list').append(noDataRow);
            }
        })
        .fail(function (error) {
            show_error_message(error.responseJSON.error);
        });
}


function deleteApiUser(user_id) {
    if (confirm('Are you sure you want to delete this user?')) {
        $.ajax({
            url: `api/delete_api_user?user_id=${user_id}`,
            type: 'DELETE',
            success: function(response) {
                show_success_message(response.success);
                get_api_user_list();
            },
            error: function(error) {
                show_error_message(error.responseJSON.error);
            }
        });
    }
}


function reset_api_user_filter(){
    $('#filter_username').val('');
    $('#filter_user_type').val('');
    get_api_user_list();
}
