from websocket_server import WebsocketServer
import logging
import json

from SuggestionApp import SuggestionApp
sApp = SuggestionApp()

def client_msg_rcvd(client, server, message):
    message = json.loads(message)
    if message['type'] == "autocomplete":
        res = sApp.getSuggestions(message['data']['query'], lang=message['data']['lang'], limit=message['data']['limit'])
        res = json.dumps({
            "msg_id": message['msg_id'],
            "response": dict(res)
        })
        server.send_message(client, res)
    else:
        raise Exception("Incorrect Msg type received")
    return

server = WebsocketServer(13254, host='127.0.0.1')
server.set_fn_message_received(client_msg_rcvd)
server.run_forever()
