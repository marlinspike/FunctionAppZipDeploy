import logging
import azure.functions as func
import json

bp = func.Blueprint()


@bp.function_name(name="write_to_queue")
@bp.route(route="write_to_queue")
@bp.queue_output(arg_name="outputQueue", queue_name="myqueue", connection="AzureWebJobsStorage")
def main(req: func.HttpRequest, outputQueue: func.Out[str]) -> func.HttpResponse:
    logging.info("HTTP trigger function to write a message to the queue.")
    
    # Get the message from the query string or default message
    message = req.params.get('message', "Hello, Azure Queue with Binding!")
    
    # Set the output queue message
    outputQueue.set(message)

    return func.HttpResponse(f"Message sent to queue: {message}")


@bp.function_name(name="read_from_queue")
@bp.queue_trigger(arg_name="msg", queue_name="myqueue", connection="AzureWebJobsStorage")
def main(msg: func.QueueMessage) -> None:
    # Get the message body
    message = msg.get_body().decode('utf-8')
    logging.info(f"Queue trigger function processed message: {message}")