// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title 3 or more out of 5 protectors can change the owner

contract ChangingOwner {

    /// @notice Candidate for changing the owner
    mapping (address => uint256) public candidates;

    /// @notice Adding votes for new owner candidate by protectors
    mapping (address => mapping(address => bool)) public alreadyVoted;

    /// @notice Candidates for changing protectors
    mapping (address => uint256) public candidatesChange;

    /// @notice Adding votes for new protectors candidates by protectors
    mapping (address => mapping(address => bool)) public alreadyVotedChange;

    /// @notice Storing the address of the current owner, so the contract inheriting this one, will be able to call it
    mapping (address => bool) public smartcontractOwner;

    /// @notice Address of the current owner
    address public newOwner;

    /// @notice Storing all protectors
    address[] internal allprotectorsaddresses;

    /// @notice Emit all the addresses of the protectors
    event showAllProtectors(address indexed _address);

    constructor(
        address _smartContractOwner,
        address _protector1, 
        address _protector2, 
        address _protector3, 
        address _protector4, 
        address _protector5 
    ){
        newOwner = _smartContractOwner;
        smartcontractOwner[_smartContractOwner] = true;

        allprotectorsaddresses.push(_protector1);
        allprotectorsaddresses.push(_protector2);
        allprotectorsaddresses.push(_protector3);
        allprotectorsaddresses.push(_protector4);
        allprotectorsaddresses.push(_protector5);

    for (uint8 i = 1; i <= 5; i++){
            candidates[_smartContractOwner] += 1;
            alreadyVoted[allprotectorsaddresses[i - 1]][_smartContractOwner] = true;
        }
    }

    /// @notice Checking if the input address is the protector
    function checkWhichProtector(address _address) internal view returns(uint8 _i){
        for (uint8 i = 0; i < 5; i++){
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
        candidates[newOwner] = 0;
        for (uint8 i = 0; i < 5; i++){
            alreadyVoted[allprotectorsaddresses[i]][newOwner] = false;
        }
        //deleting the previous owner
        smartcontractOwner[newOwner] = false;
        //change the owner
        smartcontractOwner[_nextInline] = true;
        newOwner = _nextInline;
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
        for (uint8 i = 0; i < 5; i++){
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
        for (uint8 i = 0; i < 5; i++){
            alreadyVotedChange[allprotectorsaddresses[i]][_oldAddress] = false;
        }
        //change the protector
        allprotectorsaddresses[idOfOurAddress] = _newAddress;
    }

    /// @notice Voting for candidates by protectors
    function voteForProtectorCandidate(address _nextInLine) external {
        checkWhichProtector(msg.sender);
        require(alreadyVotedChange[msg.sender][_nextInLine] == false, "You have entered your vote");
        for (uint8 i = 0; i < 5; i++){
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
    

