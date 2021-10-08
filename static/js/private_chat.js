$(document).ready(function() {
    var sender = $('input[name="sender"]').val();
    var receiver = $('input[name="receiver"]').val();
    //var chatId = $('input[name="room_id"]').val();
    var message = $('textarea#message').val();
    var display_chats = $('#display_chats')

    setInterval(function() {
        $.ajax({
            url: '/chat/get_private_messages/',
            data: {
                'sender': sender,
                'receiver': receiver
            },
            dataType: 'json',
            success: function(data) {
                console.log(data)
                display_chats.empty();
                var data_msg = data.private_details
                data_msg.map(x => {
                    display_chats.append(`
                        <p>${x.message}</p>
                        <small>on ${x.date}</small>
                        <hr>
                    `)
                })
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            }
        })
    }, 1000);

    $('form#private_form').submit(function(e) {
        e.preventDefault()
        var msg = $('textarea#message').val();
        $.ajax({
            url: "/chat/save_private/",
            data: {
                'sender': sender,
                'receiver': receiver,
                'message': msg,
            },
            dataType: 'json',
            success: function(data) {
                console.log(data.private_msg)
                $('textarea#message').val('')
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            }
        })
    })
})