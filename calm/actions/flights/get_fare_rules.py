from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from shared_tools.booking import TravelTools
from rasa_sdk.events import SlotSet, BotUttered
import json


tools = TravelTools()

class GetFareRules(Action):

    def name(self) -> Text:
        return "get_fare_rules"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Fetching fare rules included in your booking.... ")
        booking_details = dict(tracker.get_slot("booking_details"))

        fare_rules = tools.get_fare_rules(booking_details["flight"]["airline"], booking_details["flight"]["fare_class"])

        return [SlotSet("fare_rules", fare_rules)]
