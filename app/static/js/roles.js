$(document).ready(function (){
    get_roles_list();

    $('#filter_role_name').on('input', function() {
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
        $('#filter_role_name').val(selectedValue);
        $('#suggestionRoles').hide();
    });
})


function create_role_name(roleName){
    const params = {
        role_name: roleName.val()
    }
    $.get('api/create_role_name', params)
        .done(function (success) {
            show_success_message(success.success)
            roleName.val('')
            $('#createRoleModal').modal('hide');
            get_roles_list();
        })
        .fail(function (error) {
            show_error_message(error.responseJSON.error)
        });
}


function get_roles_list() {
    const params = {
        role_name: $('#filter_role_name').val(),
        created_by: $('#filter_created_by').val()
    }
    $.get('api/roles_list', params)
        .done(function (data) {
            $('#tbody_roles_list').empty();

            if (data.length > 0) {
                data.forEach(function (item) {
                    const row = `
                        <tr>
                            <td>${item.role_name}</td>
                            <td>${item.created_by}</td>
                            <td>${item.created_at}</td>
                            <td class="text-end">
                                <a class="btn btn-sm btn-success" title="API's" href="${apiListUrl}?role_name=${item.role_name}"><i class="fas fa-shield-alt"></i></a>
                                <button class="btn btn-sm btn-danger" onclick="deleteRole('${item.id}')"><i class="fas fa-trash-alt"></i></button>
                            </td>
                        </tr>
                    `;
                    $('#tbody_roles_list').append(row);
                });
            } else {
                const noDataRow = `
                    <tr>
                        <td colspan="4" class="text-center my-2">No data available</td>
                    </tr>
                `;
                $('#tbody_roles_list').append(noDataRow);
            }
        })
        .fail(function (error) {
            show_error_message(error.responseJSON.error);
        });
}


function deleteRole(roleId) {
    if (confirm('Are you sure you want to delete this role?')) {
        $.ajax({
            url: `api/delete_role?role_id=${roleId}`,
            type: 'DELETE',
            success: function(response) {
                show_success_message(response.success);
                get_roles_list();
            },
            error: function(error) {
                show_error_message(error.responseJSON.error);
            }
        });
    }
}


function reset_role_filter(){
    $('#filter_role_name').val('');
    $('#filter_created_by').val('');
    get_roles_list();
}
