from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from shared_tools.booking import TravelTools
from rasa_sdk.events import SlotSet

tools = TravelTools()

class ValidatePassportFormat(Action):

    def name(self) -> Text:
        return "validate_passport_format"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        passport_number = tracker.get_slot("passenger_passport_id")
        nationality = tracker.get_slot("passenger_nationality")
        nationality_code_map = {
            "India": "IN",
            "United States": "US",
            "Germany": "DE",
            "France": "FR",
        }
        country_code = nationality_code_map.get(nationality)

        passport_validity = tools.validate_passport_format(passport_number, country_code)

        return [SlotSet("passport_validity", passport_validity)]
