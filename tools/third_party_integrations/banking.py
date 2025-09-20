"""Banking automation placeholders."""
from typing import Dict

from agno.tools import Toolkit

from tools.common import not_implemented


def bank_check_balance(institution: str) -> Dict[str, str]:
    """Check account balance."""
    if not institution:
        raise ValueError("institution is required")
    return not_implemented(
        feature="bank_check_balance",
        integration_hint=(
            "Integrate with banking APIs via Plaid or financial institution connections with secure token handling."
        ),
    )


def bank_list_transactions(institution: str, account_id: str) -> Dict[str, str]:
    """List recent transactions."""
    if not institution:
        raise ValueError("institution is required")
    if not account_id:
        raise ValueError("account_id is required")
    return not_implemented(
        feature="bank_list_transactions",
        integration_hint=(
            "Use Plaid Transactions endpoint or institution-specific APIs with proper OAuth scopes."
        ),
    )


def bank_pay_bill(institution: str, payee: str, amount: float) -> Dict[str, str]:
    """Pay a bill from an account."""
    if not institution:
        raise ValueError("institution is required")
    if not payee:
        raise ValueError("payee is required")
    if amount <= 0:
        raise ValueError("amount must be positive")
    return not_implemented(
        feature="bank_pay_bill",
        integration_hint="Implement secure bill payment flows through bank APIs or manual automation.",
    )


class BankingToolkit(Toolkit):
    """Toolkit outlining banking features."""

    def __init__(self) -> None:
        super().__init__(name="banking")
        self.register(bank_check_balance)
        self.register(bank_list_transactions)
        self.register(bank_pay_bill)

    def instructions(self) -> str:
        return "Banking tooling requires rigorous security review and credential vaulting."


BANKING_TOOLKIT = BankingToolkit()

__all__ = ["BANKING_TOOLKIT", "BankingToolkit"]
