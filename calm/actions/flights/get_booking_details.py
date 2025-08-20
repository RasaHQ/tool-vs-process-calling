from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from shared_tools.booking import TravelTools
from rasa_sdk.events import SlotSet

tools = TravelTools()

class GetBookingDetails(Action):

    def name(self) -> Text:
        return "get_booking_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        booking_id = tracker.get_slot("booking_id")

        booking_details = tools.get_booking_details(booking_id)

        readable_booking_details = (f"Status: {booking_details['status']}\n"
                                    f"Flight ID: {booking_details['flight']['flight_id']}\n"
                                    f"Route: {booking_details['flight']['route']}\n"
                                    f"Date: {booking_details['flight']['date']}\n"
                                    f"Time: {booking_details['flight']['time']}\n"
                                    f"Passenger Name: {booking_details['passengers'][0]}\n"
                                    f"Total Paid: {booking_details['total_paid']}\n")

        return [
                    SlotSet("booking_details", booking_details),
                    SlotSet("booking_details_readable", readable_booking_details),
        ]
