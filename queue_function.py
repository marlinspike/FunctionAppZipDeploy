import logging
import azure.functions as func
import json
from azure.storage.queue import QueueClient
import os
import typing

bp = func.Blueprint()


@bp.function_name(name="write_to_queue")
@bp.route(route="write_to_queue")
@bp.queue_output(arg_name="outputQueue", queue_name="myqueue", connection="AzureWebJobsStorage")
def main(req: func.HttpRequest, outputQueue: func.Out[typing.List[str]]) -> func.HttpResponse:
    logging.info("HTTP trigger function to write a message to the queue.")
    
    # Get the message from the query string or default message
    #message = req.params.get('message', "Hello, Azure Queue with Binding!")
    messages = ["Hello", "World"]
    # Set the output queue message
    outputQueue.set(messages)
    

    return func.HttpResponse(f"Message sent to queue")


# This is just how you would have to send messages if you didn't use the queue output binding
def write_to_queue(message):
    connection_string = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"
    if not connection_string:
        raise ValueError("AzureWebJobsStorage environment variable is missing.")

    queue_name = "myqueue"

    # Create a QueueClient
    queue_client = QueueClient.from_connection_string(conn_str=connection_string, queue_name=queue_name)

    try:
        queue_client.create_queue()
        print(f"Queue '{queue_name}' created successfully.")
    except Exception as e:
        print(f"Queue '{queue_name}' already exists.")

    # Send a message to the queue
    queue_client.send_message(message)

    print("Message sent to the queue successfully.")



@bp.function_name(name="read_from_queue")
@bp.queue_trigger(arg_name="msg", queue_name="myqueue", connection="AzureWebJobsStorage")
def main(msg: func.QueueMessage) -> None:
    # Get the message body
    message = msg.get_body().decode('utf-8')
    logging.info(f"Queue trigger function processed message: {message}")