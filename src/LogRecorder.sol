// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract LogRecorder {
    event IntrusionDetected(
        string ip,
        string timestamp,
        string description
    );

    function recordIntrusion(
        string memory ip,
        string memory timestamp,
        string memory description
    ) public {
        // 把入侵事件的 IP、時間、描述公開在鏈上
        emit IntrusionDetected(ip, timestamp, description);
    }
}
