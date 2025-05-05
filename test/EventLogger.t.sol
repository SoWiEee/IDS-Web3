// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "lib/forge-std/src/Test.sol";
import {EventLogger} from "../src/EventLogger.sol";

contract EventLoggerTest is Test {
    EventLogger logger;

    function setUp() public {
        logger = new EventLogger();
    }

    // test event log
    function testRecordAndReadEvent() public {
        string memory eventType = "Process Creation";
        uint256 timestamp = block.timestamp;
        string memory image = "C:\\Windows\\System32\\cmd.exe";
        string memory commandLine = "cmd.exe /c whoami";
        string memory pid = "1234";
        string memory user = "UserA";
        string memory integrityLevel = "High";
        //string memory parentImage = "explorer.exe";

        logger.recordEvent(eventType, timestamp, image, commandLine, pid, user, integrityLevel);

        (
            string memory _eventType,
            uint256 _timestamp,
            string memory _image,
            string memory _commandLine,
            string memory _pid,
            string memory _user,
            string memory _integrityLevel
        ) = logger.getLog(0);

        assertEq(_eventType, eventType);
        assertEq(_timestamp, timestamp);
        assertEq(_image, image);
        assertEq(_commandLine, commandLine);
        assertEq(_pid, pid);
        assertEq(_user, user);
        assertEq(_integrityLevel, integrityLevel);
    }
}
