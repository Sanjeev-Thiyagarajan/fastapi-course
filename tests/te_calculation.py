import pytest
from app.calculation import add, divide, multipy, subtract, BankAccount, InsufficcientFunds


@pytest.mark.parametrize("num1, num2, expected", [
    (5, 7, 12),
    (4, 2, 6),
    (9, 8, 17)
])
def test_add(num1, num2, expected):

    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(20, 8) == 12


def test_divide():
    assert divide(9, 3) == 3


def test_multiply():
    assert multipy(3, 4) == 12


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(11, 0)


# def test_default_amount():
#     bank_account = BankAccount()
#     assert bank_account.balance == 0


# def test_set_initial_amount():
#     bank_account = BankAccount(50)
#     assert bank_account.balance == 50


# def test_withdraw():
#     bank_account = BankAccount(50)
#     bank_account.withdraw(20)
#     assert bank_account.balance == 30


# def test_deposit():
#     bank_account = BankAccount(50)
#     bank_account.deposit(30)
#     assert bank_account.balance == 80


# def test_collect_interest():
#     bank_account = BankAccount(50)
#     bank_account.collect_interest()
#     assert bank_account.balance == 50*1.1

# ------------------------------------------------------------

@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


def test_default_amount(zero_bank_account):

    assert zero_bank_account.balance == 0


def test_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_withdraw(bank_account):

    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):

    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_collect_interest(bank_account):

    bank_account.collect_interest()
    assert bank_account.balance == 50*1.1


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 50, 150),
    (80, 20, 60),
    (45, 5, 40)
])
def test_transactions(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):

    with pytest.raises(InsufficcientFunds):
        bank_account.withdraw(200)
