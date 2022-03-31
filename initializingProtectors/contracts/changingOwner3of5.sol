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

    /// @notice Address of the owner
    address public smartcontractOwner;

    /// @notice Storing all protectors
    address[] public allprotectorsaddresses;

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
        smartcontractOwner = _smartContractOwner;

        allprotectorsaddresses.push(_protector1);
        allprotectorsaddresses.push(_protector2);
        allprotectorsaddresses.push(_protector3);
        allprotectorsaddresses.push(_protector4);
        allprotectorsaddresses.push(_protector5);

    for (uint256 i = 1; i <= 5; i++){
            candidates[_smartContractOwner] += 1;
            alreadyVoted[allprotectorsaddresses[i - 1]][_smartContractOwner] = true;
        }
    }
}
    

