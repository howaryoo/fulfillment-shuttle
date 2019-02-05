#!/usr/bin/env python

import json
import logging

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
        transport_entities = req['queryResult']['parameters'].get('transport-entities')
        time_entities = req['queryResult']['parameters'].get('time-entities')
        date_param = req['queryResult']['parameters'].get('date')
        from_ = req['queryResult']['parameters'].get('from')
        to_ = req['queryResult']['parameters'].get('to')

        # TODO log properly
        print("intent: %s, params: from: %s, to: %s, when: %s" %
              (intent_display_name, from_, to_, time_entities))

        # Query schedule and get response
        time = get_time(from_, to_, time_entities, date_param)

        output = f"the {time_entities} {transport_entities} from {from_} to {to_} is leaving at {time}"

        # Compose the response to Dialogflow
        res = {'fulfillmentText': output}
    else:
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
