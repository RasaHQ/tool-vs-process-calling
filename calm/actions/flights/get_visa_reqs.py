from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from shared_tools.booking import TravelTools
from rasa_sdk.events import SlotSet

tools = TravelTools()

class ValidatePassportFormat(Action):

    def name(self) -> Text:
        return "get_visa_requirements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        nationality = tracker.get_slot("passenger_nationality")
        destination_city = tracker.get_slot("destination_city")

        entry_requirements = tools.get_visa_requirements(nationality, destination_city)


        return [SlotSet("visa_requirements", f"Visa required: {entry_requirements['visa_required']}\n"
                                                      f"Max duration of stay: {entry_requirements['max_stay_days']}")]
