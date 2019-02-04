#!/usr/bin/env python

import json

from flask import Flask, jsonify, make_response, request

from bll import get_time

app = Flask(__name__)
log = app.logger


@app.route('/webhook', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook

    """

    # Get request parameters
    req = request.get_json(force=True)
    intent = req.get('queryResult').get('intent')

    if intent and intent.get("displayName"):
        intent_display_name = intent.get("displayName")

        # Get the parameters
        # "parameters": {
        #     "transport-entities": "shuttle",
        #     "time-entities": "last",
        #     "date": ""
        # },
        transport_entities = req['queryResult']['parameters'].get('transport-entities')
        time_entities = req['queryResult']['parameters'].get('time-entities')
        date_param = req['queryResult']['parameters'].get('date')
        from_ = req['queryResult']['parameters'].get('from')
        to_ = req['queryResult']['parameters'].get('to')

        # Query schedule and get response
        time = get_time(from_, to_, time_entities, date_param)

        output = f"the {time_entities} {transport_entities} from {from_} to {to_} is leaving at {time}"

        # Compose the response to Dialogflow
        res = {'fulfillmentText': output}
    else:
        # If the request is not to the translate.text action throw an error
        log.error('Unexpected action requested: %s', json.dumps(req))
        res = {'speech': 'error', 'displayText': 'error'}

    return make_response(jsonify(res))


if __name__ == '__main__':
    PORT = 8080

    app.run(
        debug=True,
        port=PORT,
        host='0.0.0.0'
    )
