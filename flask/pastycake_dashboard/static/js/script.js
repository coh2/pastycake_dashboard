/* Author:

*/

var pollTimer, maxId=-1;

function poll_once(){
    $.ajax({ url: "/get_latest", data: {id: maxId}, dataType: "json", timeout: 12000, success: function(data) {
        if(data.id < maxId) {
            return;
        }
        else {
            maxId = data.id;
        }
        $('#matches').prepend(data.dom);
    }, error: function() {
        alert('connection failed. stopping polling.');
        clearInterval(pollTimer);
    }
    });
};

pollTimer = setInterval(poll_once, 15000);

