import json
import logging
import azure.functions as func

def main(event: func.EventGridEvent, outputSbMsg: func.Out[str]):
    logging.info("Event Grid Trigger Fired")

    try:
        data = event.get_json()
        logging.info(f"Event received: {json.dumps(data)}")

        blob_url = None

        if isinstance(data, dict):
            blob_url = data.get("url")
            if not blob_url and "data" in data and isinstance(data["data"], dict):
                blob_url = data["data"].get("url")

        if not blob_url:
            logging.error("❌ Blob URL not found in the event data")
            return

        logging.info(f"Blob URL extracted: {blob_url}")

        message = {"blob_url": blob_url}

        outputSbMsg.set(json.dumps(message))
        logging.info("✅ Message sent to Service Bus queue")

    except Exception as ex:
        logging.exception(f"Error processing event: {ex}")
