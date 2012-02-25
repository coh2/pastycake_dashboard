/* Author:

*/

(function poll(reqobj, result){
    if (result === 'error' || result === 'abort') {
        return;
    }
    $.ajax({ url: "http://127.0.0.1:5000/get_latest", success: function(data){
        $("#matches").prepend(data);
    }, dataType: "json", complete: poll, timeout: 30000 });
})(null, '');


