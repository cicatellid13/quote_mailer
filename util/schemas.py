from pydantic import BaseModel, Field


class TwilioSmsSchema(BaseModel):
    body: str = Field(..., description="sms message content")
    recipient_number: str = Field(..., description="recipient phone number")
    sender_number: str = Field(..., description="sender phone number")


class UserDbSchema(BaseModel):
    username: str = Field(..., description="unique username")
    author_choice: str = Field(..., description="current author choice")
    number: int = Field(..., description="user phone number")
    quotes_sent: dict[str, list[str]] = Field(
        default_factory=dict,
        description="quotes already sent to this user, split by author",
    )


class UserDbAddUsedQuote(BaseModel):
    username: str = Field(..., description="unique username")
    author: str = Field(..., description="author of the quote")
    quote: str = Field(..., description="quote to be added")


class QuoteDbSchema(BaseModel):
    author: str = Field(..., description="author of the quotes")
    quotes: list[str] = Field(..., description="list of quotes")
