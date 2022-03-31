// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title 3 or more out of 5 protectors can change the owner
// change the inherited addresses
//import "https://github.com/farinavito/ProtectSmartcontractChangeable/blob/main/initializingProtectors/contracts/changingOwner3of5.sol";
import "farinavito/ProtectSmartcontractChangeable@1.0.0/initializingProtectors/contracts/changingOwner3of5.sol";


contract ChangingOwnerInherited is ChangingOwner(0x33A4622B82D4c04a53e170c638B944ce27cffce3, 0x0063046686E46Dc6F15918b61AE2B121458534a5, 0x21b42413bA931038f35e7A5224FaDb065d297Ba3, 0x46C0a5326E643E4f71D3149d50B48216e174Ae84, 0x807c47A89F720fe4Ee9b8343c286Fc886f43191b, 0x844ec86426F076647A5362706a04570A5965473B){
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