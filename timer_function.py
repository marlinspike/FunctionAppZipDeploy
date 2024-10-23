import azure.functions as func
import logging
from datetime import datetime

bp = func.Blueprint()

@bp.function_name(name="TimerTrigger")
@bp.schedule(schedule="0 */5 * * * *", arg_name="timer")
def timer_trigger(timer: func.TimerRequest) -> None:
    utc_timestamp = datetime.utcnow().isoformat()
    
    if timer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
