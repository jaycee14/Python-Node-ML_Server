# Python-Node-ML_Server
A Node server / Python ML model interface 

## Rationale
For an iOS project of mine I was using a Node.JS application server that returned realtime predictions from a machine learning model. 
The model had been developed in Python using Sci-Kit Learn and this project was a way to bridge the gap.

##Overview
Essentially the Node app would connect, via a localhost TCP connection, to a Python server on the same machine. 
The data (weather forecasts in my case) was passed as JSON from the Node app, processed and predicted by the Python server using a pre computed model and returned to the Node app, also as JSON.
The Node app could then send the prediction to the user. All this happened in realtime.

## Brief File Description
###Model Holder 
Here the model data is loaded from a pickle file.

###Model Server
The Python script to run the TCP server, receives the data from the socket, processes the data into the correct format for the model, runs the data through the model and returns the predictions over the socket.

###Socket Client
The Node socket wrapped into a module for calling from the main app.

###TCP Client tests
Single run Node script (avoiding the rest of the app overhead ) to test the connection.

