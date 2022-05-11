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
        //storing the smartcontract's owner
        newOwner = _smartContractOwner;
        smartcontractOwner[_smartContractOwner] = true;

        //Storing all protectors
        allprotectorsaddresses.push(_protector1);
        allprotectorsaddresses.push(_protector2);
        allprotectorsaddresses.push(_protector3);
        allprotectorsaddresses.push(_protector4);
        allprotectorsaddresses.push(_protector5);

    //initialize the protectors
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
        //checking if the caller is one of the protectors
        checkWhichProtector(msg.sender);
        //checking if the _nextInLine has enough votes
        require(candidates[_nextInline] >= 3, "Not enough protectors agree with this address");
        //changing old values of protectors to zero and false
        candidates[newOwner] = 0;
        for (uint8 i = 0; i < 5; i++){
            alreadyVoted[allprotectorsaddresses[i]][newOwner] = false;
        }
        //changing the previous owner to false
        smartcontractOwner[newOwner] = false;
        //change the owner
        smartcontractOwner[_nextInline] = true;
        newOwner = _nextInline;
    }

    /// @notice Voting for candidates by protectors
    function voteForOwnerCandidate(address _nextInLine) external {
        //checking if the caller is one of the protectors
        checkWhichProtector(msg.sender);
        //checking if the caller hasn't already voted for _nextInLine
        require(alreadyVoted[msg.sender][_nextInLine] == false, "You have entered your vote");
        //declaring that the caller has already voted for _nextInLine
        alreadyVoted[msg.sender][_nextInLine] = true;
        //increasing the number of votes for _nextInLine
        candidates[_nextInLine] += 1;
    }

    /// @notice remove vote by the protector from previously voted protectorWaitingToBeOwner
    function removeVoteForOwnerCandidate(address _nextInLine) external {
        //checking if the caller is one of the protectors
        checkWhichProtector(msg.sender);
        //checking if the caller has already voted for _nextInLine
        require(alreadyVoted[msg.sender][_nextInLine] == true, "You haven't voted for this address");
        //declaring that the caller hasn't already voted for _nextInLine
        alreadyVoted[msg.sender][_nextInLine] = false;
        //decreasing the number of votes for _nextInLine
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
        //checking if the caller is one of the protectors
        checkWhichProtector(msg.sender);
        //storing the old protector's id
        uint256 idOfOurAddress = checkWhichProtector(_oldAddress);
        //checking if the _nextInLine has enough votes
        require(candidatesChange[_newAddress] >= 3, "Not enough protectors agree with this address");
        //changing the old values of protectors to zero and false
        candidates[_oldAddress] = 0;
        for (uint8 i = 0; i < 5; i++){
            alreadyVotedChange[allprotectorsaddresses[i]][_oldAddress] = false;
        }
        //change the protector to _newAddress
        allprotectorsaddresses[idOfOurAddress] = _newAddress;
    }

    /// @notice Voting for candidates by protectors
    function voteForProtectorCandidate(address _nextInLine) external {
        //checking if the caller is one of the protectors
        checkWhichProtector(msg.sender);
        //checking if the caller hasn't already voted for _nextInLine
        require(alreadyVotedChange[msg.sender][_nextInLine] == false, "You have entered your vote");
        //checking if _nextInLine address already exists as a protector
        for (uint8 i = 0; i < 5; i++){
            require(allprotectorsaddresses[i] != _nextInLine, "This protector already exsists");
        }
        //declaring that the caller has already voted for _nextInLine
        alreadyVotedChange[msg.sender][_nextInLine] = true;
        //increasing the number of votes for _nextInLine
        candidatesChange[_nextInLine] += 1;
    }

    /// @notice remove vote by the protector from previously voted protectorWaitingToBeOwner
    function removeVoteForProtectorCandidate(address _nextInLine) external {
        //checking if the caller is one of the protectors
        checkWhichProtector(msg.sender);
        //checking if the caller has already voted for _nextInLine
        require(alreadyVotedChange[msg.sender][_nextInLine] == true, "You haven't voted for this address");
        //declaring that the caller hasn't already voted for _nextInLine
        alreadyVotedChange[msg.sender][_nextInLine] = false;
        //decreasing the number of votes for _nextInLine
        candidatesChange[_nextInLine] -= 1;
    }
}
    

