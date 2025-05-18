// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "lib/forge-std/src/Script.sol";
import {EventLogger} from "../src/EventLogger.sol";
import {MaliciousLogger} from "../src/MaliciousLogger.sol";

contract Deploy is Script {
    function run() external {
        vm.startBroadcast();

        MaliciousLogger malicious = new MaliciousLogger();
        console.log("MaliciousLogger deployed at:", address(malicious));

        EventLogger eventLogger = new EventLogger();
        console.log("EventLogger deployed at:", address(eventLogger));

        vm.stopBroadcast();
    }
}
