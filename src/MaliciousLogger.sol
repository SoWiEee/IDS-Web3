// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract MaliciousLogger {
    struct MaliciousLog {
        string event_type;
        uint256 timestamp;
        string image;
        string command_line;
        string pid;
        string user;
        string integrity_level;
        string detail;
    }

    MaliciousLog[] public maliciousLogs;

    event MaliciousLogAdded(
        string event_type,
        uint256 timestamp,
        string image,
        string command_line,
        string pid,
        string user,
        string integrity_level,
        string detail
    );

    // struct pack
    struct MaliciousLogInput {
        string event_type;
        uint256 timestamp;
        string image;
        string command_line;
        string pid;
        string user;
        string integrity_level;
        string detail;
    }

    function addMaliciousLog(MaliciousLogInput calldata input) public {
        maliciousLogs.push(
            MaliciousLog(
                input.event_type,
                input.timestamp,
                input.image,
                input.command_line,
                input.pid,
                input.user,
                input.integrity_level,
                input.detail
            )
        );

        emit MaliciousLogAdded(
            input.event_type,
            input.timestamp,
            input.image,
            input.command_line,
            input.pid,
            input.user,
            input.integrity_level,
            input.detail
        );
    }

    function addMaliciousLog(
        string memory event_type,
        uint256 timestamp,
        string memory image,
        string memory command_line,
        string memory pid,
        string memory user,
        string memory integrity_level,
        string memory detail
    ) public {
        maliciousLogs.push(MaliciousLog(event_type, timestamp, image, command_line, pid, user, integrity_level, detail));

        emit MaliciousLogAdded(event_type, timestamp, image, command_line, pid, user, integrity_level, detail);
    }

    function getMaliciousLog(uint256 index)
        public
        view
        returns (
            string memory,
            uint256,
            string memory,
            string memory,
            string memory,
            string memory,
            string memory,
            string memory
        )
    {
        MaliciousLog memory log = maliciousLogs[index];
        return (
            log.event_type,
            log.timestamp,
            log.image,
            log.command_line,
            log.pid,
            log.user,
            log.integrity_level,
            log.detail
        );
    }

    function getLogsCount() public view returns (uint256) {
        return maliciousLogs.length;
    }
}
