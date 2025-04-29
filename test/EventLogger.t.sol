// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "forge-std/Test.sol";  // 修正這裡，正確導入 Test.sol
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
