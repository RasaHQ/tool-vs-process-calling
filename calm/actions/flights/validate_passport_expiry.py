from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from shared_tools.booking import TravelTools
from rasa_sdk.events import SlotSet

tools = TravelTools()

class ValidatePassportExpiry(Action):

    def name(self) -> Text:
        return "check_passport_expiry_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        passport_number = tracker.get_slot("passenger_passport_id")
        nationality = tracker.get_slot("passenger_nationality")
        date_of_travel = tracker.get_slot("date_of_travel")

        passport_expiry_status = tools.check_passport_expiry_status(passport_number, nationality, date_of_travel)

        return [SlotSet("passport_not_expired", passport_expiry_status["valid"])]
