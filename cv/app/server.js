var express = require('express');
var nowjs = require('now');
var Bridge = require('bridge-js');
var bridge = new Bridge({ apiKey : "c44bcbad333664b9" });
var channel;
bridge.connect();

bridge.joinChannel('gesture', { onGesture : function(gesture) { console.log("CHANNEL:", gesture); }
}, function(c) {
  channel = c;
});

var app = express.createServer();
var everyone = nowjs.initialize(app);

everyone.now.distributeMessage = function(message){
  everyone.now.receiveMessage(this.now.name, message);
};

app.use(express.static('static/'));

app.get('/api/:gest', function(req, res) {
  channel.onGesture(req.params.gest);
  res.send(200);
});

app.listen(8080);
