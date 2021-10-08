$(document).ready(function() {
    var roomName = $('input[name="room_name"]').val();
    var display_chats = $('#display_chats')

    var get_room_chats = setInterval(room_chats, 1000);

    function room_chats() {
        $.ajax({
            url: '/chat/get_room_messages/',
            data: {
                'room_name': roomName
            },
            dataType: 'json',
            success: function(data) {
                //console.log(data)
                display_chats.empty();
                var data_msg = data.message_details
                data_msg.map(x => {
                    display_chats.append(`
                        <p>${x.message}</p>
                        <small>by <div onClick=${redirect_private(x.user)}>${x.user}</div> on ${x.date}</small>
                        <hr>
                    `)
                });
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            }
        })
    };

    $('form#post_form').submit(function(e) {
        e.preventDefault()
        var username = $('input[name="username"]').val();
        var roomId = $('input[name="room_id"]').val();
        var message = $('textarea#message').val();

        $.ajax({
            url: "/chat/send/",
            data: {
                'username': username,
                'room_id': roomId,
                'message': message,
            },
            dataType: 'json',
            success: function(data) {
                $('textarea#message').val('')
                console.log(data.message_details)
                var chat_details = data.message_details
                $('#display_chats').append(`
                    <p>${chat_details.message}</p>
                    <small>by ${username} on ${chat_details.date.toLocaleString()}</small>
                    <hr>
                `)
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            }
        })
    });
    function redirect_private(friend) {
        //clearInterval(get_room_chats)
        console.log(friend)

    }
})