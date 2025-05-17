// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "lib/forge-std/src/Script.sol";
import {EventLogger} from "../src/EventLogger.sol";
import {MaliciousLogger} from "../src/MaliciousLogger.sol";

contract Deploy is Script {
    function run() external {
        vm.startBroadcast();
        new MaliciousLogger();
        new EventLogger();
        vm.stopBroadcast();
    }
}
