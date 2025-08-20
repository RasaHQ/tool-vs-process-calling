import random
from typing import List, Dict


class TravelTools:
    """Mock implementations of travel tools with realistic responses"""

    @staticmethod
    def search_flights(origin: str, destination: str, date: str, passengers: int) -> List[Dict]:
        """Mock flight search - returns fixed flight options"""
        print(f"🔍 Searching flights: {origin} → {destination} on {date} for {passengers} passengers")
        flights = [
            {
                "flight_id": "AA101",
                "airline": "American Airlines",
                "departure": f"{date} 08:00",
                "arrival": f"{date} 20:30",
                "price": 650.00,
                "seats_available": 12,
                "fare_class": "Economy"
            },
            {
                "flight_id": "DL205",
                "airline": "Delta",
                "departure": f"{date} 14:15",
                "arrival": f"{date} 02:45+1",
                "price": 720.00,
                "seats_available": 8,
                "fare_class": "Economy"
            }
        ]
        return flights

    @staticmethod
    def get_visa_requirements(passport_country: str, destination: str) -> Dict:
        """Mock visa requirements check"""
        print(f"🛂 Checking visa requirements: {passport_country} → {destination}")
        visa_required = False
        if passport_country in ["India", "IN"]:
            visa_required = True
        return {
            "visa_required": visa_required,
            "max_stay_days": 90,
            "requirements": "Valid passport with 6+ months validity",
            # "processing_time": "N/A",
            "destination_country": destination
        }

    @staticmethod
    def check_minimum_age(birth_date: str, minimum_age: int) -> bool:
        """Mock age verification"""
        print(f"📅 Checking age requirement: DOB {birth_date}, min age {minimum_age}")
        from datetime import datetime
        dob = datetime.strptime(birth_date, "%Y-%m-%d")
        age = (datetime.now() - dob).days // 365
        meets_requirement = age >= minimum_age
        print(f"   Age: {age}, Meets requirement: {meets_requirement}")
        return meets_requirement

    @staticmethod
    def get_country_entry_requirements(country_code: str) -> Dict:
        """Mock country entry requirements"""
        print(f"🌍 Getting entry requirements for: {country_code}")
        health_advisory = "All passengers must be vaccinated against Covid-19 and must show evidence of it on entry" if country_code in ["United States", "US", "Germany", "DE", "France", "FR"] else "No current health restrictions"
        return {
            "country": country_code,
            "passport_validity_months": 6,
            "vaccinations_required": [],
            "special_requirements": "None for elderly travelers",
            "health_advisory": health_advisory
        }

    @staticmethod
    def validate_passport_format(passport_number: str, country_code: str) -> bool:
        """Mock passport format validation"""
        print(f"📘 Validating passport format: {passport_number} ({country_code})")
        is_valid = len(passport_number) >= 8 and passport_number.startswith(country_code)
        print(f"   Format valid: {is_valid}")
        return is_valid

    @staticmethod
    def check_passport_expiry_status(passport_number: str, country: str, travel_date: str) -> Dict:
        """Mock passport expiry check"""
        print(f"📅 Checking passport expiry: {passport_number} for travel on {travel_date}")
        result = {
            "passport_number": passport_number,
            "valid": True,
            "expires": "2028-12-15",
            "months_remaining": 18,
            "meets_requirements": True,
            "travel_date": travel_date
        }
        print(f"   Expiry status: {result}")
        return result

    @staticmethod
    def search_hotels(city: str, checkin: str, checkout: str, rooms: int) -> List[Dict]:
        """Mock hotel search"""
        print(f"🏨 Searching hotels in {city}: {checkin} to {checkout}, {rooms} room(s)")
        return [
            {
                "hotel_id": "HTL001",
                "name": "Hotel Luxe Paris",
                "price_per_night": 180.00,
                "rating": 4.5,
                "availability": True,
                "location": "Central Paris"
            },
            {
                "hotel_id": "HTL002",
                "name": "Boutique Seine Hotel",
                "price_per_night": 220.00,
                "rating": 4.8,
                "availability": True,
                "location": "Near Louvre"
            }
        ]

    @staticmethod
    def validate_credit_card(card_number: str, expiry: str, cvv: str) -> Dict:
        """Mock credit card validation"""
        print(f"💳 Validating credit card: {card_number[-4:]} exp {expiry}")
        return {
            "valid": True,
            "card_type": "Visa",
            "issuer": "Chase Bank",
            "last_four": card_number[-4:]
        }

    @staticmethod
    def authorize_payment(card_details: Dict, amount: float) -> Dict:
        """Mock payment authorization"""
        print(f"💰 Authorizing payment: ${amount}")
        return {
            "authorized": True,
            "auth_code": f"AUTH{random.randint(100000, 999999)}",
            "amount": amount,
            "expires": "2024-03-16 08:00:00"
        }

    @staticmethod
    def create_flight_booking(flight_details: Dict, passengers: List, payment_auth: str) -> str:
        """Mock flight booking creation"""
        confirmation = f"CONF{random.randint(100000, 999999)}"
        print(f"✈️ Creating flight booking: {confirmation}")
        return confirmation

    # =============================================================================
    # FLIGHT CANCELLATION TOOLS
    # =============================================================================

    @staticmethod
    def validate_booking_reference(reference_code: str) -> bool:
        """Mock booking reference validation"""
        print(f"🔍 Validating booking reference: {reference_code}")
        # Mock: Accept any 6+ character reference starting with CONF
        is_valid = len(reference_code) >= 6 and reference_code.startswith("CONF")
        print(f"   Reference valid: {is_valid}")
        return is_valid

    @staticmethod
    def validate_passenger_name(booking_ref: str, last_name: str) -> bool:
        """Mock passenger name validation against booking"""
        print(f"👤 Validating passenger name: {last_name} for booking {booking_ref}")
        # Mock: Accept common last names for demo
        valid_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]
        is_valid = last_name in valid_names
        print(f"   Name validation: {is_valid}")
        return is_valid

    @staticmethod
    def get_booking_details(booking_reference: str) -> Dict:
        """Mock booking details retrieval"""
        print(f"📋 Retrieving booking details for: {booking_reference}")
        return {
            "booking_reference": booking_reference,
            "status": "confirmed",
            "passenger_count": 1,
            "flight": {
                "flight_id": "AA101",
                "route": "NYC-PAR",
                "date": "2025-09-15",
                "time": "08:00",
                "fare_class": "Economy",
                "price": 650.00,
                "airline": "Delta"
            },
            "total_paid": 650.00,
            "payment_method": "Visa ending in 9012",
            "booking_date": "2024-02-15",
            "passengers": ["John Smith"],
            "member_id": "AXQW123456"
        }

    @staticmethod
    def get_fare_rules(airline: str, fare_class: str) -> Dict:
        """Mock fare rules retrieval"""
        print(f"📜 Getting fare rules: {airline} {fare_class}")
        return {
            "airline": airline,
            "fare_class": fare_class,
            "cancellation_policy": {
                "24_hour_free": True,
                "before_7_days": {"fee": 200, "percentage": 0},
                "7_days_to_24_hours": {"fee": 300, "percentage": 25},
                "within_24_hours": {"fee": 400, "percentage": 50},
                "after_departure": {"fee": 0, "percentage": 100}
            },
            "refund_timeline": "7-10 business days"
        }

    @staticmethod
    def calculate_cancellation_fee(booking_ref: str, cancellation_date: str) -> Dict:
        """Mock cancellation fee calculation"""
        print(f"💰 Calculating cancellation fee for {booking_ref} on {cancellation_date}")

        # Mock calculation based on timing
        from datetime import datetime, timedelta
        cancel_date = datetime.strptime(cancellation_date, "%Y-%m-%d")
        travel_date = datetime(2025, 9, 15)  # Mock travel date
        days_before = (travel_date - cancel_date).days

        if days_before > 7:
            fee = 200
            refund_amount = 450.00  # 650 - 200
        elif days_before > 1:
            fee = 300
            refund_amount = 350.00  # 650 - 300
        else:
            fee = 400
            refund_amount = 250.00  # 650 - 400

        result = {
            "original_amount": 650.00,
            "cancellation_fee": fee,
            "refund_amount": refund_amount,
            "days_before_travel": days_before,
        }
        print(f"   Cancellation calculation: {result}")
        return result

    @staticmethod
    def check_loyalty_status(member_id: str) -> Dict:
        """Mock loyalty status check"""
        print(f"🏆 Checking loyalty status for member: {member_id}")

        # Mock: Some member IDs are platinum
        platinum_members = ["AXQW123456", "PLT789012", "PLT345678"]
        is_platinum = member_id in platinum_members

        result = {
            "member_id": member_id,
            "status": "Platinum" if is_platinum else "Gold",
        }
        print(f"   Loyalty status: {result}")
        return result

    @staticmethod
    def apply_loyalty_discount(loyalty_status: str, original_booking_amount: float, cancellation_fee: float) -> Dict:
        """Mock loyalty discount calculation"""
        if loyalty_status == "Platinum":
            return {
                "original_amount": original_booking_amount,
                "refund_amount": original_booking_amount,
            }
        else:
            return {
                "original_amount": original_booking_amount,
                "refund_amount": original_booking_amount - cancellation_fee,
            }

    @staticmethod
    def calculate_points_refund(original_amount: float, penalty_reduction: float = 0.05) -> Dict:
        """Mock points refund calculation with penalty reduction"""
        print(f"🎯 Calculating points refund: ${original_amount} with {penalty_reduction * 100}% reduction")

        # Convert to points (mock: $1 = 100 points)
        base_points = int(original_amount * 100)
        penalty_saved = original_amount * penalty_reduction
        bonus_points = int(penalty_saved * 100)
        total_points = base_points + bonus_points

        result = {
            "original_amount": original_amount,
            "penalty_reduction": penalty_reduction,
            "penalty_saved": penalty_saved,
            "base_points": base_points,
            "bonus_points": bonus_points,
            "total_points": total_points,
            "points_value": f"${total_points / 100:.2f} equivalent"
        }
        print(f"   Points calculation: {result}")
        return result

    @staticmethod
    def process_refund(booking_ref: str, amount: float, refund_method: str) -> Dict:
        """Mock refund processing"""
        print(f"💳 Processing refund: {booking_ref} - ${amount} via {refund_method}")

        transaction_id = f"REF{random.randint(100000, 999999)}"

        result = {
            "transaction_id": transaction_id,
            "booking_reference": booking_ref,
            "refund_amount": amount,
            "refund_method": refund_method,
            "processing_time": "7-10 business days" if refund_method == "original_payment" else "immediate",
            "status": "processed"
        }
        print(f"   Refund processed: {result}")
        return result

    @staticmethod
    def generate_cancellation_confirmation(booking_ref: str, refund_details: Dict) -> str:
        """Mock cancellation confirmation generation"""
        confirmation_code = f"CANC{random.randint(100000, 999999)}"
        print(f"📧 Generated cancellation confirmation: {confirmation_code}")
        return confirmation_code

    @staticmethod
    def send_cancellation_email(email: str, cancellation_details: Dict) -> bool:
        """Mock cancellation email sending"""
        print(f"📧 Sending cancellation confirmation email to: {email}")
        return True
