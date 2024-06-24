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

all_landmarks = [
    'red circle',
    'red square',
    'red triangle',
    'green circle',
    'green square',
    'green triangle',
    'blue circle',
    'blue square',
    'blue triangle'
]

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(self.name())
        dispatch_and_print(dispatcher, "I'm sorry, I don't quite understand that.")


class ActionStoreDestination(Action):
    def name(self) -> Text:
        return "action_store_destination"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        landmark = tracker.latest_message['entities'][0]["value"].lower()
        print(self.name() + f" {landmark}")

        # lets make sure it is an actual landmark
        if(landmark not in all_landmarks):
            dispatch_and_print(f"Sorry, I don't know where \"{landmark}\" is.")
            return[]
        
        # just in case we were specifically asking for location but the NLU mislabelled the entity role
        # if tracker.latest_action_name == "utter_ask_location":
        #     print(f"storing location: {landmark}")
        #     dispatch_and_print(dispatcher, template="utter_ask_location")
        #     return [SlotSet("location", landmark)]

        if(landmark in ['red triangle', 'blue square', 'green circle']):
            # since we have the destination but no location, let's ask for the location
            if tracker.slots.get("location") is None:
                dispatch_and_print(dispatcher, template="utter_ask_location")
            # we have both so its time to give directions
            else:
                location = tracker.get_slot("location").lower()
                message = get_next_target_message(location, landmark)
                dispatch_and_print(dispatcher, message)

            print(f"storing destination: {landmark}")
            return [SlotSet("destination", landmark)]
        else:
            message = f"I don't know such a destination. The possible destinations are blue square, green circle and red triangle."
            dispatch_and_print(dispatcher, message)

class ActionStoreLocation(Action):
    def name(self) -> Text:
        return "action_store_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        landmark = tracker.latest_message['entities'][0]["value"].lower()

        print(self.name() + f" {landmark}")
        
        if(landmark not in all_landmarks):
            dispatch_and_print(f"Sorry, I don't know where \"{landmark}\" is.")
            return[]
        
        # just in case we were specifically asking for location but the NLU mislabelled the entity role
        # if tracker.latest_action_name == "utter_ask_destination":
        #     print(f"storing destination: {landmark}")
        #     return [SlotSet("destination", landmark)]
        
        # since we have the location but no destination, let's ask for the destination
        if tracker.slots.get("destination") is None:
            dispatch_and_print(dispatcher, template="utter_ask_destination")
        # we have both so its time to give directions
        else:
            destination = tracker.get_slot("destination").lower()
            message = get_next_target_message(landmark, destination)
            dispatch_and_print(dispatcher, message)

        print(f"storing location: {landmark}")
        return [SlotSet("location", landmark)]
    
class ActionStoreNextLocation(Action):
    def name(self) -> Text:
        return "action_store_next_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(self.name())
        
        # lets make sure we actually have the two slots
        if tracker.slots.get("location") is None:
            # Location slot is missing, ask for location
            dispatch_and_print(dispatcher, template="utter_ask_location")
            return []
        elif tracker.slots.get("destination") is None:
            # destination slot is missing, ask for destination
            dispatch_and_print(dispatcher, template="utter_ask_destination")
            return []
        else:
            prev_location = tracker.get_slot('location').lower()
            destination = tracker.get_slot("destination").lower()
            curr_location = get_next_target(prev_location, destination)
            message = get_next_target_message(curr_location, destination)
            dispatch_and_print(dispatcher, message)

        print(f"storing location: {curr_location}")
        return [SlotSet("location", curr_location)]

class ActionStoreLocationAndDestination(Action):
    def name(self) -> Text:
        return "action_store_location_and_destination"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(self.name())
        
        landmark1 = None
        landmark2 = None
        
        if(len(tracker.latest_message['entities']) >= 1):
            landmark1 = tracker.latest_message['entities'][0]["value"].lower()
            
        if(len(tracker.latest_message['entities']) >= 2):
            landmark2 = tracker.latest_message['entities'][1]["value"].lower()
        
        print(self.name() + f" {landmark1}, {landmark2}")
        
        if tracker.slots.get("location") is None:
            # Location slot is missing, ask for location
            dispatch_and_print(dispatcher, template="utter_ask_location")
            return []
        elif tracker.slots.get("destination") is None:
            # destination slot is missing, ask for destination
            dispatch_and_print(dispatcher, template="utter_ask_destination")
            return []
        else:
            location = tracker.get_slot('location').lower()
            destination = tracker.get_slot("destination").lower()
            message = get_next_target_message(location, destination)
            dispatch_and_print(dispatcher, message)
            return []

        
        location = None
        destination = None
        
        if(landmark1 == landmark2):
            dispatch_and_print(dispatcher, "It seems like you already arrived.")
            return []
        elif(landmark1 in ['red triangle', 'blue square', 'green circle']):
            destination = landmark1
            location = landmark2
        elif(landmark2 in ['red triangle', 'blue square', 'green circle']):
            destination = landmark2
            location = landmark1
        else:
            dispatch_and_print(dispatcher, "I don't know such a destination. The possible destinations are blue square, green circle and red triangle.")
            return []
       
        message = get_next_target_message(location, destination)
        dispatch_and_print(dispatcher, message)

        print(f"storing location: {location} and destination: {destination}")
        return [SlotSet("location", location), SlotSet("destination", destination)]

class ActionUtterDestination(Action):
    def name(self) -> Text:
        return "action_utter_next_target"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(self.name())
        
        # lets make sure we actually have the two slots
        if tracker.slots.get("location") is None:
            # Location slot is missing, ask for location
            dispatch_and_print(dispatcher, template="utter_ask_location")
            return []
        elif tracker.slots.get("destination") is None:
            # destination slot is missing, ask for destination
            dispatch_and_print(dispatcher, template="utter_ask_destination")
            return []
        else:
            location = tracker.get_slot('location').lower()
            destination = tracker.get_slot("destination").lower()
            message = get_next_target_message(location, destination)
            dispatch_and_print(dispatcher, message)
            return []
    
class ActionUtterWholeRoute(Action):
    def name(self) -> Text:
        return "action_utter_whole_route"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        landmark = tracker.latest_message['entities'][0]["value"].lower()
        print(self.name() + f" {landmark}")
        
        # lets make sure it is an actual landmark
        if(landmark not in all_landmarks):
            dispatch_and_print(f"Sorry, I don't know where \"{landmark}\" is.")
            return[]
        
        # just in case we were specifically asking for location but the NLU mislabelled the entity role
        if tracker.latest_action_name == "utter_ask_location":
            print(f"storing location: {landmark}")
            return [SlotSet("location", landmark)]

        if(landmark in ['red triangle', 'blue square', 'green circle']):
            # we have both so its time to give directions
            dispatch_and_print(dispatcher, template=f"utter_whole_route_to_{landmark.replace(' ', '_')}")
            print(f"storing destination: {landmark}")
            return [SlotSet("destination", landmark)]
        else:
            message = f"That is not one of the destinations. They are the blue square, green circle and red triangle."
            dispatch_and_print(dispatcher, message)
            return []

class ActionWhereAmI(Action):
    def name(self) -> Text:
        return "action_where_am_i"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(self.name())
        
        # lets make sure we actually have the two slots
        if tracker.slots.get("location") is None and tracker.slots.get("destination") is None:
            dispatch_and_print(dispatcher, f"I don't know yet.")
        elif tracker.slots.get("location") is None:
            destination = tracker.get_slot("destination").lower()
            dispatch_and_print(dispatcher, f"You are going to {destination}, but I don't know where you are yet.")
        elif tracker.slots.get("destination") is None:
            location = tracker.get_slot('location').lower()
            dispatch_and_print(dispatcher, f"You are at {location}. I don't know where you are going though.")
        else:
            location = tracker.get_slot('location').lower()
            destination = tracker.get_slot("destination").lower()
            dispatch_and_print(dispatcher, f"You are at {location} and going to {destination}")

        return []
        
# action to repeat the last output of the robot on the user's command
# oriiginal source: https://forum.rasa.com/t/how-to-repeat-the-last-bot-utterance/4743/4
class ActionRepeat(Action):
    def name(self):
        return "action_repeat"

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        
        dispatch_and_print(dispatcher, tracker.events[-4].get('text'))
        return []
    
class ActionRestart(Action):
    def name(self):
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        print(self.name())
        
        return [SlotSet("location", None), SlotSet("destination", None)]
    
def dispatch_and_print(dispatcher, text=None, template=None, custom_payload = {}):
    if(text != None):
        print(f'OUTPUT: {text}')
        dispatcher.utter_message(text, json_message = custom_payload)
    elif(template != None):
        print(f'OUTPUT: (template) {template}')
        dispatcher.utter_message(template=template, json_message = custom_payload)   

class ActionTransferToWearable(Action):
    def name(self):
        return "action_transfer_to_wearable"

    def run(self, dispatcher, tracker, domain):
        dispatch_and_print(dispatcher, 
                           template="utter_confirm_transfer_to_watch", 
                           custom_payload= {
                                'device_instruction': 'transfer_to_wearable'
                            })

def get_next_target_message(location, destination):
    
    if(location not in all_landmarks):
        message = f"Sorry, I don't know where \"{location}\" is."
        return message

    if(destination not in all_landmarks):
        message = f"Sorry, I don't know where \"{destination}\" is."
        return message

    print(f"getting route from: {location} to: {destination}")
    
    routes = {
        'blue square': ['red circle', 'green square', 'blue triangle',  'red square', 'blue circle', 'blue square'],
        'green circle': ['red circle', 'blue triangle', 'green circle'],
        'red triangle': ['red circle', 'green triangle', 'blue square', 'blue circle', 'red triangle']
    }

    instructions = {
        'blue square': ['First, find the red circle.', 'Go left at the red circle and the green square will be on your right.', 'At the green square, the blue triangle should be behind you to your left.',  'If you continue to the right of the blue triangle, you find the red square.', 'Continue straight and the blue circle will be on your right', 'Go right at the blue circle to find the blue square.'],
        'green circle': ['First, find the red circle.', 'Go right at the red circle and then immediately left to go around the walls and the blue triangle will be ahead of you.', 'At the blue triangle, cross the doors to your left to find the green circle.'],
        'red triangle': ['First, find the red circle.', 'Go right at the red circle and follow the wall to find the green triangle to your right.', 'From the green triangle, continue left to the blue square.', 'At the blue square, turn left and find the blue circle', 'Turn right at the blue circle to find the red triangle.']
    }
    
    if(destination not in routes):
        message = f"I don't know such a destination. The possible destinations are blue square, green circle and red triangle."
    elif(location not in routes[destination]):
        message = f"You are off-path to {destination}. Return to your previous location."
    elif(routes[destination].index(location) == len(routes[destination])-1):
        message = f"You should now see your destination."
    else:
        message = instructions[destination][routes[destination].index(location) + 1]  
        
    return message

    
def get_next_target(location, destination):
    
    print(f"getting route from: {location} to: {destination}")
    
    routes = {
        'blue square': ['red circle', 'green square', 'blue triangle',  'red square', 'blue circle', 'blue square'],
        'green circle': ['red circle', 'blue triangle', 'green circle'],
        'red triangle': ['red circle', 'green triangle', 'blue square', 'blue circle', 'red triangle']
    }
    
    if(destination not in routes):
        return None
    elif(location not in routes[destination]):
        return None
    elif(routes[destination].index(location) == len(routes[destination])-1):
        return None
    else:
        return routes[destination][routes[destination].index(location) + 1]  

         
         