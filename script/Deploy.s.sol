// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "../src/LogRecorder.sol";

contract DeployScript is Script {
    function run() external {
        // 開始部署 LogRecorder 智能合約
        // 記錄入侵事件的 IP、時間、描述
        vm.startBroadcast();

        new LogRecorder();  // deployy contract
        vm.stopBroadcast(); // pause contract
    }
}