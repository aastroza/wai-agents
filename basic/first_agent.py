import asyncio
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

import workflowai
from workflowai import Model

import os
from dotenv import load_dotenv
load_dotenv()

workflowai.init( # This initialization is optional when using default settings
    api_key=os.environ.get("WORKFLOWAI_API_KEY"),  # This is the default and can be omitted
    url="https://run.workflowai.com",  # This is the default and can be omitted
)

# Input class
class EmailInput(BaseModel):
    email_content: str

# Output class
class FlightInfo(BaseModel):
    # Enum for standardizing flight status values
    class Status(str, Enum):
        """Possible statuses for a flight booking."""
        CONFIRMED = "Confirmed"
        PENDING = "Pending"
        CANCELLED = "Cancelled"
        DELAYED = "Delayed"
        COMPLETED = "Completed"

    passenger: str
    airline: str
    flight_number: str
    from_airport: str = Field(description="Three-letter IATA airport code for departure")
    to_airport: str = Field(description="Three-letter IATA airport code for arrival")
    departure: datetime
    arrival: datetime
    status: Status

# Agent definition
@workflowai.agent(
    id="flight-info-extractor",
    model=Model.GEMINI_2_0_FLASH_LATEST,
)
async def extract_flight_info(email_input: EmailInput) -> FlightInfo:
    # Agent prompt
    """
    Extract flight information from an email containing booking details.
    """
    ...


async def main():
    email = """
    Dear Jane Smith,

    Your flight booking has been confirmed. Here are your flight details:

    Flight: UA789
    From: SFO
    To: JFK
    Departure: 2024-03-25 9:00 AM
    Arrival: 2024-03-25 5:15 PM
    Booking Reference: XYZ789

    Total Journey Time: 8 hours 15 minutes
    Status: Confirmed

    Thank you for choosing United Airlines!
    """
    run = await extract_flight_info.run(EmailInput(email_content=email))
    print(run)


if __name__ == "__main__":
    asyncio.run(main())


# Output:
# ==================================================
# {
#   "passenger": "Jane Smith",
#   "airline": "United Airlines",
#   "flight_number": "UA789",
#   "from_airport": "SFO",
#   "to_airport": "JFK",
#   "departure": "2024-03-25T09:00:00",
#   "arrival": "2024-03-25T17:15:00",
#   "status": "Confirmed"
# }
# ==================================================
# Cost: $ 0.00009
# Latency: 1.18s
# URL: https://workflowai.com/_/agents/flight-info-extractor/runs/0195ee02-bdc3-72b6-0e0b-671f0b22b3dc