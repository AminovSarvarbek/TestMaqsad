import websocket
import json
import threading

# JWT token for authentication
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4ODM0ODQ1LCJpYXQiOjE3Mjg4MzM2NDUsImp0aSI6IjBkZjM5Mjg2N2Y2MDQ1NmJhYjNjZjFjOThhZTU0ZGY3IiwidXNlcl9pZCI6MiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSJ9.E3j8y4eJxShswyPVTDLPi1GBiUHz5bWbKkcXwj0LfLY"

# User ID for the WebSocket connection (the specific user the admin will chat with)
USER_ID = 2  # Update this to the user ID you are chatting with

# Callback for when a message is received from the server
def on_message(ws, message):
    data = json.loads(message)
    print(f"Data: {data}")

# Callback for WebSocket errors
def on_error(ws, error):
    print("Error:", error)

# Callback for when the WebSocket connection is closed
def on_close(ws):
    print("Connection closed")

# Callback for when the WebSocket connection is opened
def on_open(ws):
    def run(*args):
        while True:
            # Input for sending messages
            message = input("Message: ")
            # Example: Sending a message and indicating whether it's from an admin
            ws.send(json.dumps({
                'message': message,
                'is_admin': True  # Set to True if the sender is an admin, else False
            }))
    threading.Thread(target=run).start()  # Start a new thread for message input

if __name__ == "__main__":
    # WebSocket URL with the user ID and JWT token for authentication
    websocket_url = f"ws://localhost:8000/ws/chat/{USER_ID}/?token={JWT_TOKEN}"  # Update with your server's address and port
    
    # Creating WebSocket app
    ws = websocket.WebSocketApp(websocket_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    # Setting the on_open event callback
    ws.on_open = on_open
    
    # Start WebSocket client
    ws.run_forever()
