from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from shared_tools.booking import TravelTools
from rasa_sdk.events import SlotSet, BotUttered
import json


tools = TravelTools()

class GetLoyaltyStatus(Action):

    def name(self) -> Text:
        return "check_loyalty_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Checking your membership tier if you qualify for any rebates...")

        booking_details = dict(tracker.get_slot("booking_details"))

        member_id = booking_details["member_id"]

        loyalty_status = tools.check_loyalty_status(member_id)

        return [SlotSet("loyalty_status", loyalty_status)]
