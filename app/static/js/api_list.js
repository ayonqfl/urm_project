$(document).ready(function (){
    get_all_api_list();
})


function create_api(){
    const params = {
        api_role: $('#api_role_name').val(),
        api_type: $('#api_type').val(),
        api_link: $('#api_link_text').val(),
        api_details: $('#api_details').val()
    }
    $.get('api//create_api', params)
        .done(function (response) {
            $('#api_role_name').val('')
            $('#api_type').val('')
            $('#api_link_text').val('')
            $('#api_details').val('')
            show_success_message(response.success)
            $('#addAPIModal').modal('hide');
            get_all_api_list();
        })
        .fail(function (error) {
            show_error_message(error.responseJSON.error)
        });
}


function get_all_api_list() {
    const params = {
        api_role: $('#filter_api_role').val(),
        api_type: $('#filter_api_type').val(),
        api_link: $('#filter_api_link').val()
    }
    $.get('api/api_list', params)
        .done(function (data) {
            $('#tbody_api_list').empty();

            if (data.length > 0) {
                data.forEach(function (item) {
                    const row = `
                        <tr>
                            <td>${item.role_name}</td>
                            <td>${item.api}</td>
                            <td><span class="text-info fw-bold  fs-6">${item.type}</span></td>
                            <td>${item.created_at}</td>
                            <td class="text-end">
                                <button type="text" class="btn btn-sm btn-primary"><i class="fas fa-edit text-sm"></i></button>
                                <button type="text" class="btn btn-sm btn-danger"><i class="fas fa-trash-alt text-sm"></i></button>
                            </td>
                        </tr>
                    `;
                    $('#tbody_api_list').append(row);
                });
            } else {
                const noDataRow = `
                    <tr>
                        <td colspan="5" class="text-center my-2">No data available</td>
                    </tr>
                `;
                $('#tbody_api_list').append(noDataRow);
            }
        })
        .fail(function (error) {
            show_error_message(error.responseJSON.error);
        });
}


function reset_api_filter(){
    $('#filter_api_role').val('');
    $('#filter_api_link').val('');
    $('#filter_api_type').val('');
    get_all_api_list();
}