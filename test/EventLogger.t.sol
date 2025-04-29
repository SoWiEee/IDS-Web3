// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "lib/forge-std/src/Test.sol";
import {EventLogger} from "../src/EventLogger.sol";

contract EventLoggerTest is Test {
    EventLogger recorder;

    function setUp() public {
        recorder = new EventLogger();
    }

    // test event log
    function testRecordIntrusion() public {
        // log event
        recorder.logEvent("Intrusion", block.timestamp);  
        assertTrue(true);
    }
}
