<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

$db = new SQLite3('drs.db');


$instructions = [];
$result = $db->query('SELECT * FROM instructions');
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $instructions[] = $row;
}


// handle message fetching

// Takes raw data from the request
$payload = file_get_contents('php://input');

// Converts it into a PHP object
$payload = json_decode($payload);
// var_dump($payload);
$device_id = $payload->device;
foreach ($instructions as $index => $instruction) {
    if ($instruction["device"] == $device_id) {
        $i_temp = $instruction;
        $instruction_id = $instruction["id"];
        $db->exec("DELETE FROM instructions WHERE device = $device_id AND id = $instruction_id LIMIT 1");
        unset($instructions[$index]);
        echo json_encode($instruction);
        exit();
    }
}
// echo "DEBUG in POST /fetch : no instructions found for device $device";
?>