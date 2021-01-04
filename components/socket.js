// this code is not used in the app
var socket = io.connect('http://127.0.0.1:5000/')
var client = $('#username').val().substring(22)

// socket connection (sends connection check message)
socket.on('connect', function() {

	socket.emit('message', {
		user: client,
		status: 'connected'
	})

	// emits message to server (data from form) || event = message
	var form = $('form').on('submit', function(e) {
		e.preventDefault()

		let message = $('input.message').val()

		socket.emit('message', {
			user: client,
			data: message
		})

		$('input.message').val('').focus()
	})

	// emits disconnection warning to server || event = disconnection
	$('#quit').on('click', function() {
		socket.emit('disconnection', {user: client})
	})
})

// receives message from server (jquery to print message) || event = relay
socket.on('relay', function(data) {

	if (data.data !== '' && typeof data.data !== 'undefined'){

		if (data.user !== client) {
			$('#warn').remove()
			$('div.col-7').prepend('<div class="msg"><b>['+data.user+'] </b>'+data.data+'</div>')
		} else {
			$('#warn').remove()
			$('div.col-7').prepend('<div class="mymsg"><b>['+data.user+'] </b>'+data.data+'</span></div>')
		}
	}

	var counter = $('div.col-7').children('div').length;

	if (counter > 9) {
		$('div.msg').last().remove()
	}
})

// receives number of connections from server || event = online now
socket.on('online now', function(data) {

	$('#conn').remove()
	$('div.online').append('<p id="conn" style="font-size: 14px;"><i>Online agora: '+data+'</i></p>')

})
