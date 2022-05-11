# ProtectSmartcontractChangeable
Protecting smartcontracts by only enabling that 3 or more out of 5 protectors can change the owner

VISUAL REPRESENTATION
---------------------

    protector 1 ---|
    protector 2 ---|
    protector 3 ---|----- smartcontractOwner 
    protector 4 ---|      (do day to day jobs)
    protector 5 ---|



At the deployment we need to initialize:
        1) protector 1
        2) protector 2
        3) protector 3
        4) protector 4
        5) protector 5
        6) smartcontractOwner

    
FUNCTIONS OF DIFFERENT ADDRESS
------------------------------

    - protector 1-5 : They can add or remove their vote for the smartcontractOwner. They do this by calling voteForOwnerCandidate, removeVoteForOwnerCandidate and      changeOwner. 3 out of 5 protectors need to vote for a certain address to change. They can also change other protectors. 3 out of 5 protectors need to vote for a certain address to change. They do this by calling voteForProtectorCandidate, removeVoteForProtectorCandidate and changeProtector.
    - smartcontractOwner :  This address should be used in the contract that inherits this one for day to day jobs (for example: as the require that only these addresses can access a certain function)
    
    
HOW TO INCLUDE THIS CONTRACT INTO YOUR's
----------------------------------------

In your smart contract write:

    AddressProtector public accessingProtectors;

    constructor(address _address) {
        accessingProtectors = AddressProtector(_address);
    }
    
Than you can use it as: 

    require(accessingProtectors.smartcontractOwner(), "You aren't the owner");
