// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title 3 or more out of 5 protectors can change the owner
// change the inherited addresses
//import "https://github.com/farinavito/ProtectSmartcontractChangeable/blob/main/initializingProtectors/contracts/changingOwner3of5.sol";
import "farinavito/ProtectSmartcontractChangeable@1.0.0/initializingProtectors/contracts/changingOwner3of5.sol";


contract ChangingOwnerInherited is ChangingOwner(0x5B38Da6a701c568545dCfcB03FcB875f56beddC4, 0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2, 0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db, 0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB, 0x617F2E2fD72FD9D5503197092aC168c91465E7f2, 0x17F6AD8Ef982297579C203069C1DbfFE4348c372){
    /// @notice Only the smartContractOwner can access
    modifier onlySmartcontractOwner(){
        require(smartcontractOwner == msg.sender, "You are not the owner");
        _;
    }

    /// @notice Checking if the input address is the protector
    function checkWhichProtector(address _address) internal view returns(uint256 _i){
        for (uint256 i = 0; i < 5; i++){
            if (allprotectorsaddresses[i] == _address){
                return i;
            } else if (i != 4){
                continue;
            } else {
                revert("You don't have permissions");
            }
        }
    }

    /// @notice Changing the smartContractOwner
    function changeOwner(address _nextInline) external {
        checkWhichProtector(msg.sender);
        require(candidates[_nextInline] >= 3, "Not enough protectors agree with this address");
        //old values to zero and false
        candidates[smartcontractOwner] = 0;
        for (uint256 i = 0; i < 5; i++){
            alreadyVoted[allprotectorsaddresses[i]][smartcontractOwner] = false;
        }
        //change the owner
        smartcontractOwner = _nextInline;
    }

    /// @notice Voting for candidates by protectors
    function voteForOwnerCandidate(address _nextInLine) external {
        checkWhichProtector(msg.sender);
        require(alreadyVoted[msg.sender][_nextInLine] == false, "You have entered your vote");
        alreadyVoted[msg.sender][_nextInLine] = true;
        candidates[_nextInLine] += 1;
    }

    /// @notice remove vote by the protector from previously voted protectorWaitingToBeOwner
    function removeVoteForOwnerCandidate(address _nextInLine) external {
        checkWhichProtector(msg.sender);
        require(alreadyVoted[msg.sender][_nextInLine] == true, "You haven't voted for this address");
        alreadyVoted[msg.sender][_nextInLine] = false;
        candidates[_nextInLine] -= 1;
    }
  
    /// @notice Returning all addresses of protectors
    function returnProtectors() external {
        for (uint256 i = 0; i < 5; i++){
            emit showAllProtectors(allprotectorsaddresses[i]);
        }
    }

    /// @notice Changing the protector's address
    function changeProtector(address _newAddress, address _oldAddress) external {
        checkWhichProtector(msg.sender);
        uint256 idOfOurAddress = checkWhichProtector(_oldAddress);
        require(candidatesChange[_newAddress] >= 3, "Not enough protectors agree with this address");
        //old values to zero and false
        candidates[_oldAddress] = 0;
        for (uint256 i = 0; i < 5; i++){
            alreadyVotedChange[allprotectorsaddresses[i]][_oldAddress] = false;
        }
        //change the protector
        allprotectorsaddresses[idOfOurAddress] = _newAddress;
    }

    /// @notice Voting for candidates by protectors
    function voteForProtectorCandidate(address _nextInLine) external {
        checkWhichProtector(msg.sender);
        require(alreadyVotedChange[msg.sender][_nextInLine] == false, "You have entered your vote");
        for (uint256 i = 0; i < 5; i++){
            require(allprotectorsaddresses[i] != _nextInLine, "This protector already exsists");
        }
        alreadyVotedChange[msg.sender][_nextInLine] = true;
        candidatesChange[_nextInLine] += 1;
    }

    /// @notice remove vote by the protector from previously voted protectorWaitingToBeOwner
    function removeVoteForProtectorCandidate(address _nextInLine) external {
        checkWhichProtector(msg.sender);
        require(alreadyVotedChange[msg.sender][_nextInLine] == true, "You haven't voted for this address");
        alreadyVotedChange[msg.sender][_nextInLine] = false;
        candidatesChange[_nextInLine] -= 1;
    }
}