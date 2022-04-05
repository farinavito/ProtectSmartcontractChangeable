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



'''TESTING voteForOwnerCandidate'''



@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_checkWhichProtector_voteForOwnerCandidate_true(deploy, protector):
    '''checking if only protectors can access this function'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.candidates(accounts[9]) == 1

@pytest.mark.parametrize("non_protector",  [7, 8, protectorOwner])
def test_checkWhichProtector_voteForOwnerCandidate_false(deploy, non_protector):
    '''checking if others can't access this function'''
    try:
         deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[non_protector]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteForOwnerCandidate_2nd_require(deploy, protector):
    '''checking if the protector cannot vote for the same address twice'''
    try:
         deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
         deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "You have entered your vote"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteForOwnerCandidate_alreadyVoted(deploy, protector):
    '''check if alreadyVoted returns true after the protector submits its vote'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.alreadyVoted(accounts[protector], accounts[9]) == True

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteForOwnerCandidate_candidates_increment(deploy, protector):
    '''Checking if the candidates number increases after the protector submits its vote'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.candidates(accounts[9]) == 1

def test_voteForOwnerCandidate_candidates_increment_5_protectors(deploy):
    '''Checking if the candidates number increases after the protector submits its vote'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector4]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector5]})
    assert deploy.candidates(accounts[9]) == 5



'''TESTING removeVoteForOwnerCandidate'''



@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_checkWhichProtector_removeVoteForOwnerCandidate_true(deploy, protector):
    '''checking if only protectors can access this function'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.candidates(accounts[9]) == 0

@pytest.mark.parametrize("non_protector",  [7, 8, protectorOwner])
def test_checkWhichProtector_removeVoteForOwnerCandidate_false(deploy, non_protector):
    '''checking if others can't access this function'''
    try:
         deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector1]})
         deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[non_protector]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVoteForOwnerCandidate_2nd_require_not_voted(deploy, protector):
    '''checking if the protector cannot remove vote for the same address twice when you haven't vote for it'''
    try:
        deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
        deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "You haven't voted for this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVoteForOwnerCandidate_2nd_require_voted(deploy, protector):
    '''checking if the protector cannot remove vote for the same address twice'''
    try:
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
        deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
        deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "You haven't voted for this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVoteForOwnerCandidate_alreadyVoted_after_remove_protector(deploy, protector):
    '''check if alreadyVoted returns false after the protector removes its vote'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.alreadyVoted(accounts[protector], accounts[9]) == False

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVoteForOwnerCandidate_alreadyVoted_after_remove_all_protectors(deploy, protector):
    '''check if alreadyVoted returns false after the protector removes its vote'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector4]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector5]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector4]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector5]})
    assert deploy.alreadyVoted(accounts[protector], accounts[9]) == False

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVoteForOwnerCandidate_candidates_decrement_protector(deploy, protector):
    '''Checking if the candidates number decreases after the protector submits its removal vote'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.candidates(accounts[9]) == 0

def test_removeVoteForOwnerCandidate_candidates_decrement_all_protectors(deploy):
    '''Checking if the candidates number decreases after the protector submits its removal vote'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector4]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector5]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector4]})
    deploy.removeVoteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector5]})
    assert deploy.candidates(accounts[9]) == 0



'''TESTING CHANGEOWNER'''



@pytest.mark.parametrize("Owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector",  [addressProtector3, addressProtector4, addressProtector5])
def test_checkWhichProtector_changeOwner_true_part1(deploy, protector, Owner):
    '''checking if only protectors can access this function'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    deploy.changeOwner(accounts[9], {'from': accounts[Owner]})
    assert deploy.smartcontractOwner() == accounts[9]

@pytest.mark.parametrize("Owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2])
@pytest.mark.parametrize("protector2",  [addressProtector4, addressProtector5])
def test_checkWhichProtector_changeOwner_true_part2(deploy, Owner, protector, protector2):
    '''checking if only protectors can access this function'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector2]})
    deploy.changeOwner(accounts[9], {'from': accounts[Owner]})
    assert deploy.smartcontractOwner() == accounts[9]

@pytest.mark.parametrize("Owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_checkWhichProtector_changeOwner_true_part3(deploy, Owner):
    '''Checking if we can substitute the owner'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector4]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector5]})
    deploy.changeOwner(accounts[9], {'from': accounts[Owner]})
    assert deploy.smartcontractOwner() == accounts[9]

@pytest.mark.parametrize("protector",  [addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("non_protector",  [7, 8, protectorOwner])
def test_checkWhichProtector_changeOwner_false_part1(deploy, non_protector, protector):
    '''checking if others can't access this function'''
    try:
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector1]})
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector2]})
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
        deploy.changeOwner(accounts[9], {'from': accounts[non_protector]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2])
@pytest.mark.parametrize("protector2",  [addressProtector4, addressProtector5])
@pytest.mark.parametrize("non_protector",  [7, 8, protectorOwner])
def test_checkWhichProtector_changeOwner_false_part2(deploy, non_protector, protector, protector2):
    '''checking if others can't access this function'''
    try:
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector2]})
        deploy.changeOwner(accounts[9], {'from': accounts[non_protector]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

@pytest.mark.parametrize("non_protector",  [7, 8, protectorOwner])
def test_checkWhichProtector_changeOwner_false_part3(deploy, non_protector):
    '''checking if others can't access this function'''
    try:
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector4]})
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector5]})
        deploy.changeOwner(accounts[9], {'from': accounts[non_protector]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeowner_2nd_require_fail_no_vote(deploy, protector):
    '''checking if this function can be called after 3 or more protectors agree'''
    try:
        deploy.changeOwner(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "Not enough protectors agree with this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector2",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeowner_2nd_require_fail_1_vote(deploy, protector, protector2):
    '''checking if this function can be called after 3 or more protectors agree'''
    try:
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
        deploy.changeOwner(accounts[9], {'from': accounts[protector2]})
    except Exception as e:
        assert e.message[50:] == "Not enough protectors agree with this address"

'''
all combinations of checking the 2nd require statement when 2 voters
1 2
1 3
1 4
1 5
2 5
3 2
3 4
3 5
4 2
4 5
'''

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector2",  [addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeowner_2nd_require_fail_2_votes_part1(deploy, protector, protector2):
    '''checking if this function can be called after 3 or more protectors agree'''
    try:
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector1]})
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector2]})
        deploy.changeOwner(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "Not enough protectors agree with this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector2",  [addressProtector2, addressProtector4, addressProtector5])
def test_changeowner_2nd_require_fail_2_votes_part2(deploy, protector, protector2):
    '''checking if this function can be called after 3 or more protectors agree'''
    try:
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector2]})
        deploy.changeOwner(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "Not enough protectors agree with this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector2",  [addressProtector2, addressProtector5])
def test_changeowner_2nd_require_fail_2_votes_part3(deploy, protector, protector2):
    '''checking if this function can be called after 3 or more protectors agree'''
    try:
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector4]})
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector2]})
        deploy.changeOwner(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "Not enough protectors agree with this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeowner_2nd_require_fail_2_votes_part4(deploy, protector):
    '''checking if this function can be called after 3 or more protectors agree'''
    try:
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector5]})
        deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector2]})
        deploy.changeOwner(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "Not enough protectors agree with this address"

'''
all combinations of changing owner
1 2 3
1 2 4
1 2 5
1 3 4
1 3 5
2 3 4
2 3 5
3 4 5
'''

@pytest.mark.parametrize("Owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector",  [addressProtector3, addressProtector4, addressProtector5])
def test_changeowner_success_part1(deploy, Owner, protector):
    '''Checking if we can substitute the owner'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    deploy.changeOwner(accounts[9], {'from': accounts[Owner]})
    assert deploy.smartcontractOwner() == accounts[9]

@pytest.mark.parametrize("Owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2])
@pytest.mark.parametrize("protector2",  [addressProtector4, addressProtector5])
def test_changeowner_success_part2(deploy, Owner, protector, protector2):
    '''Checking if we can substitute the owner'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector2]})
    deploy.changeOwner(accounts[9], {'from': accounts[Owner]})
    assert deploy.smartcontractOwner() == accounts[9]

@pytest.mark.parametrize("Owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeowner_success_part3(deploy, Owner):
    '''Checking if we can substitute the owner'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector4]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector5]})
    deploy.changeOwner(accounts[9], {'from': accounts[Owner]})
    assert deploy.smartcontractOwner() == accounts[9]

@pytest.mark.parametrize("Owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector",  [addressProtector3, addressProtector4, addressProtector5])
def test_changeowner_old_owner_part1(deploy, Owner, protector):
    '''Checking if the candidate's number for old owner is equal to 0'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    deploy.changeOwner(accounts[9], {'from': accounts[Owner]})
    assert deploy.candidates(accounts[protectorOwner]) == 0

@pytest.mark.parametrize("Owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2])
@pytest.mark.parametrize("protector2",  [addressProtector4, addressProtector5])
def test_changeowner_old_owner_part2(deploy, Owner, protector, protector2):
    '''Checking if the candidate's number for old owner is equal to 0'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector2]})
    deploy.changeOwner(accounts[9], {'from': accounts[Owner]})
    assert deploy.candidates(accounts[protectorOwner]) == 0

@pytest.mark.parametrize("Owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeowner_old_owner_part3(deploy, Owner):
    '''Checking if the candidate's number for old owner is equal to 0'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector4]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector5]})
    deploy.changeOwner(accounts[9], {'from': accounts[Owner]})
    assert deploy.candidates(accounts[protectorOwner]) == 0

@pytest.mark.parametrize("Owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector",  [addressProtector3, addressProtector4, addressProtector5])
def test_changeowner_old_owner_alreadyVoted_part1(deploy, Owner, protector):
    '''Checking if the alreadyVoted for old owner is equal to false'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    deploy.changeOwner(accounts[9], {'from': accounts[Owner]})
    assert deploy.alreadyVoted(accounts[Owner], accounts[protectorOwner]) == False

@pytest.mark.parametrize("Owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2])
@pytest.mark.parametrize("protector2",  [addressProtector4, addressProtector5])
def test_changeowner_old_owner_alreadyVoted_part2(deploy, Owner, protector, protector2):
    '''Checking if the alreadyVoted for old owner is equal to 0'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[protector2]})
    deploy.changeOwner(accounts[9], {'from': accounts[Owner]})
    assert deploy.alreadyVoted(accounts[Owner], accounts[protectorOwner]) == False

@pytest.mark.parametrize("Owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeowner_old_owner_alreadyVoted_part3(deploy, Owner):
    '''Checking if the alreadyVoted for old owner is equal to 0'''
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector4]})
    deploy.voteForOwnerCandidate(accounts[9], {'from': accounts[addressProtector5]})
    deploy.changeOwner(accounts[9], {'from': accounts[Owner]})
    assert deploy.alreadyVoted(accounts[Owner], accounts[protectorOwner]) == False



'''TESTING RETURNPROTECTORS'''



def test_returnProtectors_1(deploy):
    '''Checking if this function really emits correct addresses'''
    function_initialize = deploy.returnProtectors()
    assert function_initialize.events[0][0]['_address'] == accounts[addressProtector1]

def test_returnProtectors_2(deploy):
    '''Checking if this function really emits correct addresses'''
    function_initialize = deploy.returnProtectors()
    assert function_initialize.events[1][0]['_address'] == accounts[addressProtector2]

def test_returnProtectors_3(deploy):
    '''Checking if this function really emits correct addresses'''
    function_initialize = deploy.returnProtectors()
    assert function_initialize.events[2][0]['_address'] == accounts[addressProtector3]

def test_returnProtectors_4(deploy):
    '''Checking if this function really emits correct addresses'''
    function_initialize = deploy.returnProtectors()
    assert function_initialize.events[3][0]['_address'] == accounts[addressProtector4]

def test_returnProtectors_5(deploy):
    '''Checking if this function really emits correct addresses'''
    function_initialize = deploy.returnProtectors()
    assert function_initialize.events[4][0]['_address'] == accounts[addressProtector5]



'''TESTING CHANGEPROTECTOR'''



@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("oldProtector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_checkWhichProtector_changeProtectore_true(deploy, protector, oldProtector):
    '''checking if only protectors can access this function'''
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.changeProtector(accounts[9], accounts[oldProtector], {'from': accounts[protector]})
    assert deploy.allprotectorsaddresses(oldProtector - 2) == accounts[9]

@pytest.mark.parametrize("non_protector",  [7, 8, protectorOwner])
@pytest.mark.parametrize("oldProtector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_checkWhichProtector_changeProtectore_false(deploy, non_protector, oldProtector):
    '''checking if others can't access this function'''
    try:
        deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[addressProtector1]})
        deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[addressProtector2]})
        deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[addressProtector3]})
        deploy.changeProtector(accounts[9], accounts[oldProtector], {'from': accounts[non_protector]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("oldProtector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeProtector_2nd_require(deploy, protector, oldProtector):
    '''Checking if enough protectors have voted for this candidate '''
    try:
        deploy.changeProtector(accounts[9], accounts[oldProtector], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "Not enough protectors agree with this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("oldProtector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeProtector_2nd_require_same_voters(deploy, protector, oldProtector):
    '''Checking if enough protectors have voted for this candidate '''
    try:
        deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
        deploy.changeProtector(accounts[9], accounts[oldProtector], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "Not enough protectors agree with this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("other_protector",  [addressProtector5, addressProtector4, addressProtector2, addressProtector3, addressProtector1])
@pytest.mark.parametrize("oldProtector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeProtector_2nd_require_different_voters_1vote(deploy, protector, oldProtector, other_protector):
    '''Checking if enough protectors have voted for this candidate '''
    try:
        deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
        deploy.changeProtector(accounts[9], accounts[oldProtector], {'from': accounts[other_protector]})
    except Exception as e:
        assert e.message[50:] == "Not enough protectors agree with this address"

@pytest.mark.parametrize("combo", [[addressProtector1, addressProtector5], [addressProtector1, addressProtector4], [addressProtector1, addressProtector3], [addressProtector1, addressProtector2], [addressProtector2, addressProtector5], [addressProtector2, addressProtector4], [addressProtector2, addressProtector3], [addressProtector2, addressProtector1], [addressProtector3, addressProtector5], [addressProtector3, addressProtector4], [addressProtector3, addressProtector2], [addressProtector3, addressProtector1], [addressProtector4, addressProtector5], [addressProtector4, addressProtector3], [addressProtector4, addressProtector2], [addressProtector4, addressProtector1], [addressProtector5, addressProtector4], [addressProtector5, addressProtector3], [addressProtector5, addressProtector2], [addressProtector5, addressProtector1]])
@pytest.mark.parametrize("oldProtector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeProtector_2nd_require_different_voters_2votes(deploy, combo, oldProtector):
    '''Checking if enough protectors have voted for this candidate '''
    try:
        deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[combo[0]]})
        deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[combo[1]]})
        deploy.changeProtector(accounts[9], accounts[oldProtector], {'from': accounts[combo[1]]})
    except Exception as e:
        assert e.message[50:] == "Not enough protectors agree with this address"

@pytest.mark.parametrize("combo", [[2, 6, 3], [2, 6, 4], [2, 6, 5], [2, 5, 3], [2, 5, 4], [2, 5, 6], [2, 4, 3], [2, 4, 5], [2, 4, 6], [2, 3, 4], [2, 3, 5], [2, 3, 6], [3, 6, 2], [3, 6, 4], [3, 6, 5], [3, 5, 2], [3, 5, 4], [3, 5, 6], [3, 4, 2], [3, 4, 5], [3, 4, 6], [3, 2, 4], [3, 2, 5], [3, 2, 6], [4, 6, 2], [4, 6, 3], [4, 6, 5], [4, 5, 2], [4, 5, 3], [4, 5, 6], [4, 3, 2], [4, 3, 5], [4, 3, 6], [4, 2, 3], [4, 2, 5], [4, 2, 6], [5, 6, 2], [5, 6, 3], [5, 6, 4], [5, 4, 2], [5, 4, 3], [5, 4, 6], [5, 3, 2], [5, 3, 4], [5, 3, 6], [5, 2, 3], [5, 2, 4], [5, 2, 6], [6, 5, 2], [6, 5, 3], [6, 5, 4], [6, 4, 2], [6, 4, 3], [6, 4, 5], [6, 3, 2], [6, 3, 4], [6, 3, 5], [6, 2, 3], [6, 2, 4], [6, 2, 5]])
@pytest.mark.parametrize("change",  [[2, 6], [2, 5], [2, 4], [2, 3], [2, 2], [3, 6], [3, 5], [3, 4], [3, 3], [3, 2], [4, 6], [4, 5], [4, 4], [4, 3], [4, 2], [5, 6], [5, 5], [5, 4], [5, 3], [5, 2], [6, 6], [6, 5], [6, 4], [6, 3], [6, 2]])
@pytest.mark.parametrize("oldProtector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeProtector_modifies_allprotectorsaddresses(deploy, combo, change, oldProtector):
    '''Checking if the protector in allprotectorsaddresses is changed to the new address'''
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[combo[0]]})
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[combo[1]]})
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[combo[2]]})
    deploy.changeProtector(accounts[9], accounts[oldProtector], {'from': accounts[change[0]]})
    assert deploy.allprotectorsaddresses(oldProtector - 2) == accounts[9]

@pytest.mark.parametrize("combo", [[2, 6, 3], [2, 6, 4], [2, 6, 5], [2, 5, 3], [2, 5, 4], [2, 5, 6], [2, 4, 3], [2, 4, 5], [2, 4, 6], [2, 3, 4], [2, 3, 5], [2, 3, 6], [3, 6, 2], [3, 6, 4], [3, 6, 5], [3, 5, 2], [3, 5, 4], [3, 5, 6], [3, 4, 2], [3, 4, 5], [3, 4, 6], [3, 2, 4], [3, 2, 5], [3, 2, 6], [4, 6, 2], [4, 6, 3], [4, 6, 5], [4, 5, 2], [4, 5, 3], [4, 5, 6], [4, 3, 2], [4, 3, 5], [4, 3, 6], [4, 2, 3], [4, 2, 5], [4, 2, 6], [5, 6, 2], [5, 6, 3], [5, 6, 4], [5, 4, 2], [5, 4, 3], [5, 4, 6], [5, 3, 2], [5, 3, 4], [5, 3, 6], [5, 2, 3], [5, 2, 4], [5, 2, 6], [6, 5, 2], [6, 5, 3], [6, 5, 4], [6, 4, 2], [6, 4, 3], [6, 4, 5], [6, 3, 2], [6, 3, 4], [6, 3, 5], [6, 2, 3], [6, 2, 4], [6, 2, 5]])
@pytest.mark.parametrize("change",  [[2, 6], [2, 5], [2, 4], [2, 3], [2, 2], [3, 6], [3, 5], [3, 4], [3, 3], [3, 2], [4, 6], [4, 5], [4, 4], [4, 3], [4, 2], [5, 6], [5, 5], [5, 4], [5, 3], [5, 2], [6, 6], [6, 5], [6, 4], [6, 3], [6, 2]])
@pytest.mark.parametrize("oldProtector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeProtector_old_candidates_0(deploy, combo, change, oldProtector):
    '''Checking if the old candidateChange for the protector is 0'''
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[combo[0]]})
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[combo[1]]})
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[combo[2]]})
    deploy.changeProtector(accounts[9], accounts[oldProtector], {'from': accounts[change[0]]})
    assert deploy.candidatesChange(accounts[protectorOwner]) == 0

@pytest.mark.parametrize("combo", [[2, 6, 3], [2, 6, 4], [2, 6, 5], [2, 5, 3], [2, 5, 4], [2, 5, 6], [2, 4, 3], [2, 4, 5], [2, 4, 6], [2, 3, 4], [2, 3, 5], [2, 3, 6], [3, 6, 2], [3, 6, 4], [3, 6, 5], [3, 5, 2], [3, 5, 4], [3, 5, 6], [3, 4, 2], [3, 4, 5], [3, 4, 6], [3, 2, 4], [3, 2, 5], [3, 2, 6], [4, 6, 2], [4, 6, 3], [4, 6, 5], [4, 5, 2], [4, 5, 3], [4, 5, 6], [4, 3, 2], [4, 3, 5], [4, 3, 6], [4, 2, 3], [4, 2, 5], [4, 2, 6], [5, 6, 2], [5, 6, 3], [5, 6, 4], [5, 4, 2], [5, 4, 3], [5, 4, 6], [5, 3, 2], [5, 3, 4], [5, 3, 6], [5, 2, 3], [5, 2, 4], [5, 2, 6], [6, 5, 2], [6, 5, 3], [6, 5, 4], [6, 4, 2], [6, 4, 3], [6, 4, 5], [6, 3, 2], [6, 3, 4], [6, 3, 5], [6, 2, 3], [6, 2, 4], [6, 2, 5]])
@pytest.mark.parametrize("change",  [[2, 6], [2, 5], [2, 4], [2, 3], [2, 2], [3, 6], [3, 5], [3, 4], [3, 3], [3, 2], [4, 6], [4, 5], [4, 4], [4, 3], [4, 2], [5, 6], [5, 5], [5, 4], [5, 3], [5, 2], [6, 6], [6, 5], [6, 4], [6, 3], [6, 2]])
@pytest.mark.parametrize("oldProtector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeProtector_old_candidates_alreadyVoted(deploy, combo, change, oldProtector):
    '''Checking if the alreadyVoted for old owner is equal to false'''
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[combo[0]]})
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[combo[1]]})
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[combo[2]]})
    deploy.changeProtector(accounts[9], accounts[oldProtector], {'from': accounts[change[0]]})
    assert deploy.alreadyVotedChange(accounts[oldProtector], accounts[protectorOwner]) == False



'''TESTING voteForProtectorCandidate'''



@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_checkWhichProtector_voteForProtectorCandidate_true(deploy, protector):
    '''checking if only protectors can access this function'''
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.candidatesChange(accounts[9]) == 1

@pytest.mark.parametrize("non_protector",  [7, 8, protectorOwner])
def test_checkWhichProtector_voteForProtectorCandidate_false(deploy, non_protector):
    '''checking if others can't access this function'''
    try:
        deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[non_protector]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteForProtectorCandidate_2nd_require(deploy, protector):
    '''Checking if only protectors who didnnot vote before can access this function'''
    try:
        deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
        deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "You have entered your vote"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
@pytest.mark.parametrize("protector2",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteForProtectorCandidate_3rd_require(deploy, protector, protector2):
    '''Checking if protectors cannot vote for exsisting protectors'''
    try:
        deploy.voteForProtectorCandidate(accounts[protector2], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "This protector already exsists"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteForProtectorCandidate_alreadyVotedChange_initial(deploy, protector):
    '''Checking if alreadyVoted is initialized to False'''
    assert deploy.alreadyVotedChange(accounts[protector], accounts[9]) == False

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteForProtectorCandidate_alreadyVotedChange(deploy, protector):
    '''Checking if alreadyVoted is modified to true'''
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.alreadyVotedChange(accounts[protector], accounts[9]) == True

def test_voteForProtectorCandidate_candidates_initialized(deploy):
    '''Checking if the candidate is initialized to 0'''
    assert deploy.candidatesChange(accounts[9]) == 0

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteForProtectorCandidate_candidates_increment(deploy, protector):
    '''Checking if the candidate is incremenet'''
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.candidatesChange(accounts[9]) == 1



'''TESTING REMOVEVOTEFORPROTECTORCANDIDATE'''


@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_checkWhichProtector_removeVoteForProtectorCandidate_true(deploy, protector):
    '''checking if only protectors can access this function'''
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
    deploy.removeVoteForProtectorCandidate(accounts[9], {'from': accounts[protector]}) == "ok"
    assert deploy.candidatesChange(accounts[9]) == 0

@pytest.mark.parametrize("non_protector",  [7, 8, protectorOwner])
def test_checkWhichProtector_removeVoteForProtectorCandidate_false(deploy, non_protector):
    '''checking if others can't access this function'''
    try:
        deploy.removeVoteForProtectorCandidate(accounts[9], {'from': accounts[non_protector]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVoteForProtectorCandidate_2nd_require_not_voted(deploy, protector):
    '''Checking if only protectors who have voted for this candidate can decrease the candidate number'''
    try:
        deploy.removeVoteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "You haven't voted for this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVoteForProtectorCandidate_2nd_require_voted(deploy, protector):
    '''Checking if only protectors who have voted for this candidate can decrease the candidate number'''
    try:
        deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
        deploy.removeVoteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
        deploy.removeVoteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "You haven't voted for this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVoteForProtectorCanddate_alreadyVotedChange_initial(deploy, protector):
    '''Checking if alreadyVotedChange is initialized to False'''
    assert deploy.alreadyVotedChange(accounts[protector], accounts[9]) == False

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVoteForProtectorCandidate_alreadyVotedChange(deploy, protector):
    '''Checking if alreadyVotedChange modifies to False'''
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
    deploy.removeVoteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.alreadyVotedChange(accounts[protector], accounts[9]) == False

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVoteForProtectorCandidate_candidates_decrease(deploy, protector):
    '''Checking if candidates number decreases'''
    deploy.voteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
    deploy.removeVoteForProtectorCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.candidatesChange(accounts[9]) == 0



