# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionTransferToWearable(Action):
    def name(self):
        return "action_transfer_to_wearable"

    def run(self, dispatcher, tracker, domain):
        dispatch_and_print(dispatcher, "Okay. Let's continue on your device.", {
            'device_instruction': 'transfer_to_wearable'
        })
        
# action to repeat the last output of the robot on the user's command
# oriiginal source: https://forum.rasa.com/t/how-to-repeat-the-last-bot-utterance/4743/4
class ActionRepeat(Action):
    def name(self):
        return "action_repeat"

    def run(self, dispatcher, tracker, domain):
        dispatch_and_print(dispatcher, tracker.events[-4].get('text'))
        return []

def dispatch_and_print(dispatcher, text, custom_payload = {}):
    print(f'OUTPUT: {text}')
    dispatcher.utter_message(text, json_message = custom_payload)