// this code is not used in the app
var socket = io.connect('http://127.0.0.1:5000/')
var client = $('#username').val().substring(22)

// socket connection (sends connection check message)
socket.on('connect', function() {
	socket.emit('my event', {
		conn: 'User Connected'
	})

	// emits message to server (data from form) event = my event
	var form = $('form').on('submit', function(e) {
		e.preventDefault()

		let name = $('input.user').val()
		let message = $('input.message').val()

		socket.emit('my event', {
			user: name.substring(22),
			data: message
		})

		$('input.message').val('').focus()

	})
})

// receives message from server (jquery to print message) event = my response
socket.on('my response', function(data) {
	console.log(data)

	if (data.data !== '' && typeof data.user !== 'undefined'){

		if (data.user !== client) {
			$('#warn').remove()
			$('div.col-7').prepend('<div class="msg"><b>['+data.user+'] </b>'+data.data+'</div>')
		} else {
			$('#warn').remove()
			$('div.col-7').prepend('<div class="mymsg"><b>['+data.user+'] </b>'+data.data+'</div>')
		}
	}

	var counter = $('div.col-7').children('div').length;

	if (counter > 9) {
		$('div.msg').last().remove()
	}
})