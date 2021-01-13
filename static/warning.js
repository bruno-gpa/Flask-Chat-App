$('#send').on('click', function() {
	
	var str = $('#user').val()
	var num = $('#room').val()

	if (!/^[a-zA-Z() ]*$/.test(str)) {
		$('#help').html('<b>ERRO: nome inválido</b>').css('color', 'green')
	} else if (isNaN(num)) {
		$('#help').html('<b>ERRO: sala inválida</b>').css('color', 'green')
	}
})