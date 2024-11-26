$(document).ready(function (){
    get_roles_of_api_list();
})


function create_role_name(roleName){
    const params = {
        role_name: roleName.val()
    }
    $.get('api/create_role_name', params)
        .done(function (success) {
            show_success_message(success.success)
            roleName.val('')
            get_roles_of_api_list();
        })
        .fail(function (error) {
            show_error_message(error.responseJSON.error)
        });
}


function get_roles_of_api_list() {
    $.get('api/roles_api_list')
        .done(function (data) {
            $('#tbody_roles_api_list').empty();

            if (data.length > 0) {
                data.forEach(function (item) {
                    const row = `
                        <tr>
                            <td>${item.role_name}</td>
                            <td>${item.created_by}</td>
                            <td>${item.created_at}</td>
                            <td class="text-end">
                                <button class="btn btn-sm btn-success" title="API Activity" onclick="create_role_api('${item.role_name}')" data-bs-toggle="modal" data-bs-target="#addAPIModal"><i class="fas fa-shield-alt"></i></button>
                                <button class="btn btn-sm btn-danger" onclick="show_error_message('Are you sure you want to delete ${item.role_name}?')"><i class="fas fa-trash-alt"></i></button>
                            </td>
                        </tr>
                    `;
                    $('#tbody_roles_api_list').append(row);
                });
            } else {
                const noDataRow = `
                    <tr>
                        <td colspan="4" class="text-center">No data available</td>
                    </tr>
                `;
                $('#tbody_roles_api_list').append(noDataRow);
            }
        })
        .fail(function (error) {
            show_error_message(error.responseJSON.error);
        });
}


function create_role_api(role_name) {
    $('#modalRoleName').text(role_name);
}
