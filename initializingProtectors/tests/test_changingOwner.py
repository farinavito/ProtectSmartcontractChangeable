import pytest
import brownie
from brownie import *
from brownie import accounts

#addresses
protectorOwner = 1
addressProtector1 = 2
addressProtector2 = 3
addressProtector3 = 4
addressProtector4 = 5
addressProtector5 = 6

numCombo = 0

@pytest.fixture()
def deploy(ChangingOwner, module_isolation):
    return ChangingOwner.deploy(accounts[protectorOwner], accounts[addressProtector1], accounts[addressProtector2], accounts[addressProtector3], accounts[addressProtector4], accounts[addressProtector5], {'from': accounts[0]})


'''TESTING INITIALIZATION'''



def test_protector1_address(deploy):
    '''checking if the protector's address is correct'''
    assert deploy.allprotectorsaddresses(addressProtector1 - 2) == accounts[addressProtector1]

def test_protector2_address(deploy):
    '''checking if the protector's address is correct'''
    assert deploy.allprotectorsaddresses(addressProtector2 - 2) == accounts[addressProtector2]

def test_protector3_address(deploy):
    '''checking if the protector's address is correct'''
    assert deploy.allprotectorsaddresses(addressProtector3 - 2) == accounts[addressProtector3]

def test_protector4_address(deploy):
    '''checking if the protector's address is correct'''
    assert deploy.allprotectorsaddresses(addressProtector4 - 2) == accounts[addressProtector4]

def test_protector5_address(deploy):
    '''checking if the protector's address is correct'''
    assert deploy.allprotectorsaddresses(addressProtector5 - 2) == accounts[addressProtector5]

def test_protector6_initialization_address(deploy):
    '''testing protector 6 address when added to constructor'''
    try:
         deploy.allprotectorsaddresses(6) == "0x0000000000000000000000000000000000000000"
    except Exception as e:
        assert e.message[50:] == ""

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_protector_alreadyVoted_owner_true(deploy, protector):
    '''checking if the the protector has initialized alreadyVoted to true'''
    assert deploy.alreadyVoted(accounts[protector], accounts[protectorOwner]) == True

def test_alreadyvoted_protector6(deploy):
    '''check if protector6 will fail for already voted when initialize'''
    assert deploy.alreadyVoted(accounts[9], accounts[protectorOwner]) == False

def test_alreadyvoted_protector7(deploy):
    '''check if protector7 will fail for already voted when initialize'''
    assert deploy.alreadyVoted(accounts[protectorOwner], accounts[protectorOwner]) == False


def test_smartContractOwner(deploy):
    '''checking if the smartContractOwner is initialize'''
    assert deploy.smartcontractOwner() == accounts[protectorOwner]

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_candidates_initialized_addressProtector(deploy, protector):
    '''testing if addressProtector is initialized to 0'''
    assert deploy.candidates(accounts[protector]) == 0

def test_candidates_smartContractOwner_initialized(deploy):
    '''checking if smartContractOwner has already have 5 votes at initialization'''
    assert deploy.candidates(accounts[protectorOwner]) == 5



