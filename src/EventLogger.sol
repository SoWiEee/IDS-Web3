// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract EventLogger {
    struct Log {
        string eventType;
        uint256 timestamp;
        string image;
        string commandLine;
        string pid;
        string user;
        string integrityLevel;
    }

    Log[] public logs;

    event SecurityEvent(
        string eventType,
        uint256 timestamp,
        string image,
        string commandLine,
        string pid,
        string user,
        string integrityLevel
    );

    function recordEvent(
        string memory eventType,
        uint256 timestamp,
        string memory image,
        string memory commandLine,
        string memory pid,
        string memory user,
        string memory integrityLevel
    ) public {
        logs.push(Log(eventType, timestamp, image, commandLine, pid, user, integrityLevel));
        emit SecurityEvent(eventType, timestamp, image, commandLine, pid, user, integrityLevel);
    }

    function getLogCount() public view returns (uint256) {
        return logs.length;
    }

    function getLog(uint256 index)
        public
        view
        returns (string memory, uint256, string memory, string memory, string memory, string memory, string memory)
    {
        require(index < logs.length, "Index out of bounds");
        Log memory log = logs[index];
        return (log.eventType, log.timestamp, log.image, log.commandLine, log.pid, log.user, log.integrityLevel);
    }
}
