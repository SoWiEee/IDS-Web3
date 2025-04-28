pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import "../src/LogRecorder.sol";

contract LogRecorderTest is Test {
    LogRecorder recorder;

    function setUp() public {
        recorder = new LogRecorder();
    }

    function testRecordIntrusion() public {
        recorder.recordIntrusion("127.0.0.1", "2025-04-28 12:00:00", "Test intrusion");
        assertTrue(true);   // no revert => OK
    }
}
