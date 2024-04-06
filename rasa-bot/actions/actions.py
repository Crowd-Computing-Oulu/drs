# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

class ActionAskDestination(Action):
    def name(self) -> Text:
        return "action_ask_destination"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("What is your destination?")
        return []

class ActionStoreDestination(Action):
    def name(self) -> Text:
        return "action_store_destination"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.latest_message['entities'][0]["value"]
        if(destination in ['red triangle', 'blue square', 'green circle']):
            print(f"storing destination: {destination}")
            return [SlotSet("destination", destination)]
        else:
            message = f"I don't know such a destination. The possible destinations are blue square, green circle and red triangle."
            dispatch_and_print(dispatcher, message)

class ActionStoreLocation(Action):
    def name(self) -> Text:
        return "action_store_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = tracker.latest_message['entities'][0]["value"]
        print(f"storing location: {location}")
        return [SlotSet("location", location)]

class ActionUtterDestination(Action):
    def name(self) -> Text:
        return "action_utter_destination"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = tracker.get_slot('location')
        destination = tracker.get_slot("destination")
        message = get_next_target_message(location, destination)
        dispatch_and_print(dispatcher, message)
        return []
    
class ActionWhereAmI(Action):
    def name(self) -> Text:
        return "action_where_am_i"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = tracker.get_slot('location')
        destination = tracker.get_slot("destination")
       
        dispatch_and_print(dispatcher, f"You are at {location} and going to {destination}")
        return []
        
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
    
    
def get_next_target_message(location, destination):
    
    print(f"getting route from: {location} to: {destination}")
    
    routes = {
        'blue square': ['red circle', 'green square', 'blue triangle',  'red square', 'blue circle', 'blue square'],
        'green circle': ['red circle', 'blue triangle', 'green circle'],
        'red triangle': ['red circle', 'green triangle', 'blue square', 'blue circle', 'red triangle']
    }
    
    if(destination not in routes):
        message = f"I don't know such a destination. The possible destinations are blue square, green circle and red triangle."
    elif(location not in routes[destination]):
        message = f"You are off-path to {destination}. Return to your previous location."
    elif(routes[destination].index(location) == len(routes[destination])-1):
        message = f"You should now see your destination."
    else:
        next_landmark = routes[destination][routes[destination].index(location) + 1]  
        message = f"Next, go to {next_landmark}."
        
    return message
         