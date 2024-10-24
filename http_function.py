import azure.functions as func
import logging
import json

bp = func.Blueprint()

@bp.function_name(name="HttpTrigger")
@bp.route(route="hello")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
            name = req_body.get('name')
        except ValueError:
            pass

    if name:
        return func.HttpResponse(
            json.dumps({
                "message": f"Hello, {name}!"
            }),
            mimetype="application/json"
        )
    else:
        return func.HttpResponse(
            json.dumps({
                "error": "Please pass a name on the query string or in the request body"
            }),
            status_code=400,
            mimetype="application/json"
        )