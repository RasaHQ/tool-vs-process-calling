from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from shared_tools.booking import TravelTools
from rasa_sdk.events import SlotSet, BotUttered
import json
from datetime import datetime

tools = TravelTools()

class ApplyLoyaltyDiscount(Action):

    def name(self) -> Text:
        return "apply_loyalty_discount"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Applying loyalty discount based on your membership tier")

        loyalty_status = tracker.get_slot("loyalty_status")
        cancellation_fee_details = tracker.get_slot("cancellation_fee_details")

        refund_details = tools.apply_loyalty_discount(loyalty_status["status"],
                                                      cancellation_fee_details["original_amount"],
                                                      cancellation_fee_details["cancellation_fee"]
                                                      )

        return [SlotSet("refund_details", refund_details)]
