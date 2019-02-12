#!/usr/bin/env python

import json
from pprint import pprint

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
    # TODO debug log
    print("request:", pprint(req))

    if intent and intent.get("displayName"):
        intent_display_name = intent.get("displayName")
        transport_entities, time_entities, date_param, from_, to_, delta_amount, delta_unit = (None, ) * 7

        # Get the parameters
        output_contexts = req['queryResult'].get('outputContexts')
        # TODO get context name from DF ('selected')
        selected_context = [c for c in output_contexts if 'selected' in c['name']][0]

        if 'find' in intent_display_name:
            transport_entities = req['queryResult']['parameters'].get('transport-entities')
            time_entities = req['queryResult']['parameters'].get('time-entities')
            date_param = req['queryResult']['parameters'].get('time')
            from_ = req['queryResult']['parameters'].get('from')
            to_ = req['queryResult']['parameters'].get('to')
        elif 'adjust' in intent_display_name:
            if selected_context:
                transport_entities = selected_context['parameters'].get('transport-entities')
                time_entities = selected_context['parameters'].get('time-entities')
                date_param = selected_context['parameters'].get('time')
                from_ = selected_context['parameters'].get('from')
                to_ = selected_context['parameters'].get('to')

            duration = req['queryResult']['parameters'].get('duration')
            if duration:
                duration = duration[0]
                delta_amount = duration.get('amount')
                delta_unit = duration.get('unit')

        # TODO log properly
        print(f"all parameters: {req['queryResult']['parameters']}")
        print("intent: %s, params: from: %s, to: %s, when: %s, delta: %s, unit: %s" %
              (intent_display_name, from_, to_, time_entities, delta_amount, delta_unit))

        # Query schedule and get response
        returned_time = None
        if selected_context:
            returned_time = selected_context['parameters'].get('returned-time')
            print(f"returned_time received from context: {returned_time}")
        time = get_time(from_, to_, time_entities, date_param, delta_amount, delta_unit, returned_time)
        # Always update the output context with the returned time
        selected_context['parameters']['returned-time'] = time

        if time:
            output = f"the requested {transport_entities} from {from_} to {to_} is leaving at {time}"
        else:
            output = f"No schedule from {from_} to {to_} available"

        print(f"Output: {output}")

        # Compose the response to Dialogflow
        # FIXME: only one context returned
        res = {'fulfillmentText': output,
               'outputContexts': [selected_context]}
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
