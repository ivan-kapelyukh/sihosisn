from enum import Enum


class LegalType(Enum):
    PRIVATE = 0
    BUISNESS = 1


class AccountType(Enum):
    CHECKING = 0
    SAVINGS = 1


class QuoteType(Enum):
    BALANCE_PAYOUT = 0  # for payments funded from borderless account
    BALANCE_CONVERSION = 1  # for conversion between balances
    REGULAR = 2  # for payments funded via bank transfers
