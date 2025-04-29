// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import {EventLogger} from "../src/EventLogger.sol";

contract Deploy is Script {
    function run() external {
        vm.startBroadcast();
        new EventLogger();
        vm.stopBroadcast();
    }
}