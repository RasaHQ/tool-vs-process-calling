import json
import os
from typing import Dict, List, Any
from openai import OpenAI

from calm.shared_tools.booking import TravelTools

# Set your OpenAI API key
# export OPENAI_API_KEY="your-api-key-here"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =============================================================================
# MOCK TOOL IMPLEMENTATIONS (Data layer - still mocked for demo)
# =============================================================================


# =============================================================================
# FUNCTION SCHEMAS FOR OPENAI FUNCTION CALLING
# =============================================================================

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_flights",
            "description": "Search for available flights between two cities",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "Origin city code (e.g., NYC, LAX)"},
                    "destination": {"type": "string", "description": "Destination city code (e.g., PAR, LON)"},
                    "date": {"type": "string", "description": "Travel date in YYYY-MM-DD format"},
                    "passengers": {"type": "integer", "description": "Number of passengers"}
                },
                "required": ["origin", "destination", "date", "passengers"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_visa_requirements",
            "description": "Check visa requirements for travel between countries",
            "parameters": {
                "type": "object",
                "properties": {
                    "passport_country": {"type": "string",
                                         "description": "Passport issuing country code (e.g., US, UK)"},
                    "destination": {"type": "string", "description": "Destination country code (e.g., FR, IT)"}
                },
                "required": ["passport_country", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_minimum_age",
            "description": "Verify if a person meets minimum age requirements",
            "parameters": {
                "type": "object",
                "properties": {
                    "birth_date": {"type": "string", "description": "Date of birth in YYYY-MM-DD format"},
                    "minimum_age": {"type": "integer", "description": "Minimum age requirement"}
                },
                "required": ["birth_date", "minimum_age"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_country_entry_requirements",
            "description": "Get entry requirements for a specific country",
            "parameters": {
                "type": "object",
                "properties": {
                    "country_code": {"type": "string", "description": "Country code (e.g., FR, IT, US)"}
                },
                "required": ["country_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "validate_passport_format",
            "description": "Validate passport number format for a country",
            "parameters": {
                "type": "object",
                "properties": {
                    "passport_number": {"type": "string", "description": "Passport number"},
                    "country_code": {"type": "string", "description": "Issuing country code"}
                },
                "required": ["passport_number", "country_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_passport_expiry_status",
            "description": "Check if passport is valid for travel date",
            "parameters": {
                "type": "object",
                "properties": {
                    "passport_number": {"type": "string", "description": "Passport number"},
                    "country": {"type": "string", "description": "Issuing country code"},
                    "travel_date": {"type": "string", "description": "Travel date in YYYY-MM-DD format"}
                },
                "required": ["passport_number", "country", "travel_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_hotels",
            "description": "Search for available hotels in a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "checkin": {"type": "string", "description": "Check-in date YYYY-MM-DD"},
                    "checkout": {"type": "string", "description": "Check-out date YYYY-MM-DD"},
                    "rooms": {"type": "integer", "description": "Number of rooms needed"}
                },
                "required": ["city", "checkin", "checkout", "rooms"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "validate_credit_card",
            "description": "Validate credit card information",
            "parameters": {
                "type": "object",
                "properties": {
                    "card_number": {"type": "string", "description": "Credit card number"},
                    "expiry": {"type": "string", "description": "Expiry date MM/YY"},
                    "cvv": {"type": "string", "description": "CVV security code"}
                },
                "required": ["card_number", "expiry", "cvv"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "authorize_payment",
            "description": "Authorize payment for a booking",
            "parameters": {
                "type": "object",
                "properties": {
                    "card_details": {"type": "object", "description": "Credit card details"},
                    "amount": {"type": "number", "description": "Payment amount"}
                },
                "required": ["card_details", "amount"]
            }
        }
    },
    # Flight Cancellation Tools
    {
        "type": "function",
        "function": {
            "name": "validate_booking_reference",
            "description": "Validate if a booking reference exists in the system",
            "parameters": {
                "type": "object",
                "properties": {
                    "reference_code": {"type": "string", "description": "Booking reference code"}
                },
                "required": ["reference_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "validate_passenger_name",
            "description": "Validate passenger name against booking record",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_ref": {"type": "string", "description": "Booking reference"},
                    "last_name": {"type": "string", "description": "Passenger last name"}
                },
                "required": ["booking_ref", "last_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_booking_details",
            "description": "Retrieve complete booking information",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Booking reference code"}
                },
                "required": ["booking_reference"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_fare_rules",
            "description": "Get cancellation and change rules for airline fare",
            "parameters": {
                "type": "object",
                "properties": {
                    "airline": {"type": "string", "description": "Airline code or name"},
                    "fare_class": {"type": "string", "description": "Fare class (Economy, Business, First)"}
                },
                "required": ["airline", "fare_class"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_cancellation_fee",
            "description": "Calculate cancellation fees based on timing and fare rules",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_ref": {"type": "string", "description": "Booking reference"},
                    "cancellation_date": {"type": "string", "description": "Date of cancellation YYYY-MM-DD"},
                },
                "required": ["booking_ref", "cancellation_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "apply_loyalty_discount",
            "description": "Apply loyalty discount based on membership tier",
            "parameters": {
                "type": "object",
                "properties": {
                    "loyalty_status": {"type": "string", "description": "Loyalty status"},
                    "original_booking_amount": {"type": "number", "description": "Original booking amount"},
                    "cancellation_fee": {"type": "number", "description": "Cancellation fee"},
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_loyalty_status",
            "description": "Check customer loyalty program status and benefits",
            "parameters": {
                "type": "object",
                "properties": {
                    "member_id": {"type": "string", "description": "Loyalty program member ID"}
                },
                "required": ["member_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_points_refund",
            "description": "Calculate refund amount in points with penalty reduction",
            "parameters": {
                "type": "object",
                "properties": {
                    "original_amount": {"type": "number", "description": "Original refund amount"},
                    "penalty_reduction": {"type": "number",
                                          "description": "Penalty reduction percentage (default 0.05)"}
                },
                "required": ["original_amount"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "process_refund",
            "description": "Process refund to original payment method or as points",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_ref": {"type": "string", "description": "Booking reference"},
                    "amount": {"type": "number", "description": "Refund amount"},
                    "refund_method": {"type": "string", "description": "Refund method: 'original_payment' or 'points'"}
                },
                "required": ["booking_ref", "amount", "refund_method"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_cancellation_confirmation",
            "description": "Generate cancellation confirmation code",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_ref": {"type": "string", "description": "Booking reference"},
                    "refund_details": {"type": "object", "description": "Refund processing details"}
                },
                "required": ["booking_ref", "refund_details"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_cancellation_email",
            "description": "Send cancellation confirmation email",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Customer email address"},
                    "cancellation_details": {"type": "object", "description": "Cancellation and refund details"}
                },
                "required": ["email", "cancellation_details"]
            }
        }
    }
]


# =============================================================================
# REAL LLM TRAVEL AGENT
# =============================================================================

class RealLLMTravelAgent:
    def __init__(self):
        self.tools = TravelTools()
        self.conversation_history = []
        self.flight_booking_guideline = """
1. Always search for flights when users mention specific travel plans
2. Always check all entry requirements (like visa, health) for international travel.
3. Validate all passenger information including passports
4. For elderly passengers, check special requirements
5. Once all the information is given, ask for user confirmation and then go to next step
6. Verify payment methods before processing bookings
"""
        self.flight_cancellation_guidelines = """
1. Validate booking reference and passenger name for authentication
2. Retrieve booking details to show flights in the booking.
3. Always let the user confirm the booking to cancel.
4. Get fare rules and calculate cancellation fee based on membership tier.
7. Get user confirmation
8. Offer points refund option with 5% penalty reduction
9. Process refund and generate confirmation
"""
        self.flight_checkin_guidelines = """
1. Ask the user for booking reference and their last name
2. Display the booking information and ask the user for confirmation
3. Ask for passport and nationality details
4. Check all entry requirements (like visa, health) for international travel.
5. Let users pick a seat or opt for an upgrade.
6. Let users pay for any extras they have chosen.        
"""
        self._construct_system_prompt()

    def _construct_system_prompt(self):
        self.system_prompt = f"""You are a professional travel booking assistant. Help users book flights, hotels, and other travel services. You can also help with flight cancellations and refunds.

FLIGHT BOOKING GUIDELINES: {self.flight_booking_guideline}

FLIGHT CANCELLATION PROCESS: {self.flight_cancellation_guidelines}

FLIGHT CHECKIN GUIDELINES: {self.flight_checkin_guidelines}

When users provide travel details, use the available tools to:
- Search for flights and pricing
- Check visa and entry requirements  
- Validate passenger documents
- Search for accommodations if requested
- Process payments securely
- Handle cancellations and refunds

Always use tools rather than guessing or providing outdated information."""

    def update_booking_guidelines(self, new_guidelines):
        self.flight_booking_guideline = new_guidelines
        self._construct_system_prompt()

    def update_cancellation_guidelines(self, new_guidelines):
        self.flight_cancellation_guidelines = new_guidelines
        self._construct_system_prompt()

    def update_checkin_guidelines(self, new_guidelines):
        self.flight_cancellation_guidelines = new_guidelines
        self._construct_system_prompt()

    def get_system_prompt(self):
        return self.system_prompt

    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool function"""
        if hasattr(self.tools, tool_name):
            tool_func = getattr(self.tools, tool_name)
            result = tool_func(**kwargs)
            return result
        else:
            return {"error": f"Tool {tool_name} not found"}

    def process_function_calls(self, function_calls: List) -> List[Dict]:
        """Process function calls from the LLM"""
        results = []

        for call in function_calls:
            function_name = call.function.name
            function_args = json.loads(call.function.arguments)

            print(f"🔧 LLM called: {function_name}({function_args})")

            # Execute the function
            result = self.call_tool(function_name, **function_args)

            results.append({
                "call_id": call.id,
                "function_name": function_name,
                "arguments": function_args,
                "result": result
            })

        return results

    def react_loop(self, user_message: str) -> str:
        """Real ReAct loop with LLM making decisions"""
        from time import time
        print(f"\n" + '\033[1m' + f"💬 User: {user_message}" + '\033[0m')
        print("="*25)

        start = time()
        # Add conversation history
        messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history + [
            {"role": "user", "content": user_message}]

        max_iterations = 10

        for iteration in range(max_iterations):
            print(f"\n🤔 Iteration {iteration + 1}: LLM deciding what to do...")

            # Get LLM response with potential function calls
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",  # Let LLM decide when to use tools
                temperature=0.1
            )

            message = response.choices[0].message

            # Check if LLM wants to call functions
            if message.tool_calls:
                print(f"💭 LLM decided to call {len(message.tool_calls)} tool(s)")

                # Add LLM's function call message to conversation
                messages.append({
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": call.id,
                            "type": "function",
                            "function": {
                                "name": call.function.name,
                                "arguments": call.function.arguments
                            }
                        } for call in message.tool_calls
                    ]
                })

                # Process function calls
                function_results = self.process_function_calls(message.tool_calls)

                # Add function results to conversation
                for result in function_results:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": result["call_id"],
                        "content": json.dumps(result["result"])
                    })

                # Continue loop - LLM might want to call more functions
                continue

            else:
                # LLM is ready to respond to user
                print("💭 LLM decided to respond to user")
                response_text = message.content
                break

        else:
            response_text = "I apologize, but I'm having trouble processing your request. Could you please try again?"

        end = time()
        print("="*25)
        print(f"\n" + '\033[1m' + f"🤖 Agent: {response_text}" + '\033[0m')
        print(f"\n Time to respond: {round(end - start, 2)} seconds")
        print("=" * 25)
        # Update conversation history
        self.conversation_history.extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": response_text}
        ])

        return response_text


# Interactive mode
def interactive_mode():
    """Run in interactive mode for testing"""
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY environment variable")
        return

    agent = RealLLMTravelAgent()
    print("🤖 Real LLM Travel Agent - Interactive Mode")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye! 👋")
            break

        try:
            agent.react_loop(user_input)
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    interactive_mode()
