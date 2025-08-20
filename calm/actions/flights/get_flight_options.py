from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from shared_tools.booking import TravelTools
from rasa_sdk.events import SlotSet

tools = TravelTools()

class GetFlightOptions(Action):

    def name(self) -> Text:
        return "get_flight_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        source_city = tracker.get_slot("source_city")
        destination_city = tracker.get_slot("destination_city")
        num_passengers = 1
        date_of_travel = tracker.get_slot("date_of_travel")

        flight_options = tools.search_flights(source_city, destination_city, date_of_travel, num_passengers)

        readable_options = "\n\n".join([f"Flight ID: {option['flight_id']}\n"
                                          f"Departure: {option['departure']}\n"
                                          f"Arrival: {option['arrival']}\n"
                                          f"Airlines: {option['airline']}\n"
                                          f"Price: {option['price']}\n"
                                          for option in flight_options])
        return [SlotSet("flight_options", flight_options), SlotSet("flight_options_readable", readable_options)]
