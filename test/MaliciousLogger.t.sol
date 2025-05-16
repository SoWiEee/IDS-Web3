// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "lib/forge-std/src/Test.sol";
import {MaliciousLogger} from "../src/MaliciousLogger.sol";

contract MaliciousLoggerTest is Test {
    MaliciousLogger logger;

    function setUp() public {
        logger = new MaliciousLogger();
    }

    function testAddAndGetMaliciousLog() public {
        MaliciousLogger.MaliciousLogInput memory input = MaliciousLogger.MaliciousLogInput({
            event_type: "DLL Injection",
            timestamp: block.timestamp,
            image: "C:\\Windows\\System32\\malicious.dll",
            command_line: "somecommand.exe /inject",
            pid: "5678",
            user: "AdminUser",
            integrity_level: "High",
            detail: "Injected via CreateRemoteThread"
        });

        logger.addMaliciousLog(input);

        (
            string memory _eventType,
            uint256 _timestamp,
            string memory _image,
            string memory _commandLine,
            string memory _pid,
            string memory _user,
            string memory _integrityLevel,
            string memory _detail
        ) = logger.getMaliciousLog(0);

        assertEq(_eventType, input.event_type);
        assertEq(_timestamp, input.timestamp);
        assertEq(_image, input.image);
        assertEq(_commandLine, input.command_line);
        assertEq(_pid, input.pid);
        assertEq(_user, input.user);
        assertEq(_integrityLevel, input.integrity_level);
        assertEq(_detail, input.detail);
    }
}
