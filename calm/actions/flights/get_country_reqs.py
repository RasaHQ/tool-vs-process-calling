from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from shared_tools.booking import TravelTools
from rasa_sdk.events import SlotSet

tools = TravelTools()

class ValidatePassportFormat(Action):

    def name(self) -> Text:
        return "get_country_entry_requirements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        destination_city = tracker.get_slot("destination_city")
        destination_country = {"new york": "United States",
                               "new delhi": "India",
                               "berlin": "Germany",
                               "paris": "France"}.get(destination_city.lower())

        entry_requirements = tools.get_country_entry_requirements(destination_country)


        return [SlotSet("country_entry_requirements", f"{entry_requirements['special_requirements']}\n"
                                                      f"{entry_requirements['health_advisory']}")]
