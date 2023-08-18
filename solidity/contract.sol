pragma solidity ^0.8.2;

//SPDX-License-Identifier: MIT

contract Request{
    address payable owner;
    address payable courier;
    address customer;
    uint price;

    enum State{
        CREATED,
        PAYED,
        PENDING,
        COMPLETE
    }

    mapping ( State => string ) state_names;

    State tmpState;

    modifier required_state ( State state ) {
        require (
            tmpState == state,
            string.concat ( "Current state is: ", state_names[tmpState] )
        );

        _;
    }

    error InvalidCustomer();

    constructor(address _customer, uint _price) {
        customer = _customer;
        price = _price;
        tmpState = State.CREATED;

        state_names[State.COMPLETE] = "COMPLETE";
        state_names[State.CREATED] = "CREATED";
        state_names[State.PAYED] = "PAYED";
        state_names[State.PENDING] = "PENDING";

        owner = payable(msg.sender);
    }

    function pay() external payable required_state(State.CREATED){
        require(msg.sender == customer, "Invalid customer!");
        require(msg.value == price, "Invalid amount!");
        tmpState = State.PAYED;
    }

    function get_delivery(address _courier) external required_state(State.PAYED){
        require(msg.sender == owner, "Invalid owner!");
        courier = payable(_courier);
        tmpState = State.PENDING;
    }

    function delivered() external required_state(State.PENDING){
        require(msg.sender == customer, "Invalid customer!");
        uint owner_amount = 4 * price / 5;
        owner.transfer(owner_amount);
        courier.transfer(price - owner_amount);
        tmpState = State.COMPLETE;
    }


}