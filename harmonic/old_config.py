server_endpoint = "http://76.93.130.85:80/harmonic"

chat_interface_html_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 10px;
            background-color: #2d2b2b;
        }
        .chat-body {
            border-radius: 10px;
            padding: 10px;
            overflow-y: auto;
        }
        .messageincoming, .messageoutgoing {
            display: block; /* Ensures each message is on its own line */
            padding: 12px 20px;
            border-radius: 15px;
            font-size: 14px;
            line-height: 1.5;
            word-wrap: break-word;
            margin: 10px 0; /* Adds vertical spacing between messages */
            width: fit-content; /* Dynamically size the message bubble to fit the text */
            max-width: 75%; /* Optional: limit max width for better appearance */
        }
        .messageincoming {
            background-color: rgba(255,255,255,0);
            color: white;
            text-align: left;
            border-bottom-left-radius: 0; /* Square corner for alignment */
        }
        .messageoutgoing {
            background-color: rgba(255,255,255,0);
            color: #981118;
            text-align: right;
            border-bottom-right-radius: 0; /* Square corner for alignment */
            margin-left: auto; /* Align outgoing messages to the right */
        }
    </style>
</head>
'''