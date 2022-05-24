var express = require('express')
var app = express()

app.set('port', (process.env.PORT || 4000))
app.use(express.static(__dirname + '/public'))

app.get('/', function(request, response) {
  var data = new Date();
  var dia = String(data.getDate()).padStart(2, '0');
  var mes = String(data.getMonth() + 1).padStart(2, '0');
  var ano = data.getFullYear();
  dataAtual = dia + '/' + mes + '/' + ano;
  response.send('Voce esta acessando na data: ' + dataAtual)
})

app.listen(app.get('port'), function() {
  console.log("Node app is running at localhost:" + app.get('port'))
})
