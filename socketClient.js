var net = require('net');

var HOST = '127.0.0.1';
var PORT = 13373;

var client = new net.Socket();

var responseCB;

// Add a 'data' event handler for the client socket
// data is what the server sent to this socket
client.on('data', function(data) {
          
          //console.log('DATA: ' + data);
          // Close the client socket completely
          client.destroy();
          
          var jsonData =  data.toString();   //defaults are good
          
          responseCB(JSON.parse(jsonData));
          
          });

client.on('end', function() {
          console.log('Connection end');
          });


// Add a 'close' event handler for the client socket
client.on('close', function() {
          console.log('Connection closed');
          });

module.exports={

sendForecast: function(forcastData,cb){
    
    responseCB = cb;

    client.connect(PORT, HOST, function() {
                   
                   console.log('CONNECTED TO: ' + HOST + ':' + PORT);
                   // Write a message to the socket as soon as the client is connected, the server will receive it as message from the client
                   //client.write(data);
                   
                   //console.log(forcastData);
                   
                   var jsonString =JSON.stringify(forcastData);
                   
                   console.log(jsonString.length);
                   
                   //console.log(jsonString);
                   
                   client.write(jsonString);
                   
                   });
        
}



}