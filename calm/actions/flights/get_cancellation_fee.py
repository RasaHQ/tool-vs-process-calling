from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from shared_tools.booking import TravelTools
from rasa_sdk.events import SlotSet, BotUttered
import json
from datetime import datetime

tools = TravelTools()

class CalculateCancellationFee(Action):

    def name(self) -> Text:
        return "calculate_cancellation_fee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Calculating your cancellation fee based on the above...")

        booking_details = dict(tracker.get_slot("booking_details"))
        cancellation_date = datetime.now().strftime("%Y-%m-%d")

        cancellation_fee_details = tools.calculate_cancellation_fee(booking_details["booking_reference"],
                                                                    cancellation_date)

        return [SlotSet("cancellation_fee_details", cancellation_fee_details)]
