// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract EventLogger {
    event SecurityEvent(string eventType, uint256 timestamp);

    struct Log {
        string eventType;
        uint256 timestamp;
    }

    Log[] public logs;

    function logEvent(string memory eventType, uint256 timestamp) public {
        logs.push(Log(eventType, timestamp));
        emit SecurityEvent(eventType, timestamp);
    }

    function getLogCount() public view returns (uint) {
        return logs.length;
    }

    function getLog(uint256 index) public view returns (string memory, uint256) {
        require(index < logs.length, "Index out of range");
        Log memory log = logs[index];
        return (log.eventType, log.timestamp);
    }
}