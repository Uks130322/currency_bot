import dataclasses
import pytest

from extensions import Currency, UserException


@dataclasses.dataclass
class Case:
    given_name: str
    name: str
    code: str
    quantity: float
    printed_name: str

    def __str__(self) -> str:
        return f"currency_{self.given_name}"


@dataclasses.dataclass
class ErrorCase:
    given_name: str
    result: Exception


TEST_CASES = [
    Case(given_name="доллар", name="доллар", code="USD", quantity=1, printed_name="доллар"),
    Case(given_name="долларов", name="доллар", code="USD", quantity=1.14, printed_name="доллар"),
    Case(given_name="долл.", name="доллар", code="USD", quantity=2, printed_name="доллара"),
    Case(given_name="доллары", name="доллар", code="USD", quantity=4.28, printed_name="доллара"),
    Case(given_name="доллар", name="доллар", code="USD", quantity=17, printed_name="долларов"),
    Case(given_name="доллар", name="доллар", code="USD", quantity=114.92, printed_name="долларов"),
    Case(given_name="доллары", name="доллар", code="USD", quantity=230, printed_name="долларов"),

    Case(given_name="евро", name="евро", code="EUR", quantity=4.28, printed_name="евро"),
    Case(given_name="евро", name="евро", code="EUR", quantity=780, printed_name="евро"),

    Case(given_name="рубль", name="рубль", code="RUB", quantity=1, printed_name="рубль"),
    Case(given_name="рубля", name="рубль", code="RUB", quantity=110, printed_name="рублей"),
    Case(given_name="руб", name="рубль", code="RUB", quantity=13.72, printed_name="рублей"),
    Case(given_name="рубли", name="рубль", code="RUB", quantity=288.72, printed_name="рублей"),
    Case(given_name="рублей", name="рубль", code="RUB", quantity=132, printed_name="рубля"),
    Case(given_name="рубль", name="рубль", code="RUB", quantity=24, printed_name="рубля")
]

TEST_ERROR_CASES = [
    ErrorCase(given_name="р", result=UserException),
    ErrorCase(given_name="сруб", result=UserException),
    ErrorCase(given_name="рублииеще", result=UserException),
    ErrorCase(given_name="дол", result=UserException),
    ErrorCase(given_name="удолл", result=UserException),
    ErrorCase(given_name="долларизация", result=UserException),
    ErrorCase(given_name="ев", result=UserException),
    ErrorCase(given_name="европейский", result=UserException)
]


@pytest.mark.parametrize("t", TEST_CASES, ids=str)
def test_name(t: Case) -> None:
    cur = Currency(t.given_name)
    assert cur.name == t.name and cur.code == t.code


@pytest.mark.parametrize("t", TEST_ERROR_CASES, ids=str)
def test_error_name(t: ErrorCase) -> None:
    try:
        Currency(t.given_name)
    except Exception as error:
        assert type(error) == t.result


@pytest.mark.parametrize("t", TEST_CASES, ids=str)
def test_print(t: Case) -> None:
    cur = Currency(t.given_name)
    assert cur.print_quantity(t.quantity) == t.printed_name
