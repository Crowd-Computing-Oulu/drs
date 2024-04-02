<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);


$db = new SQLite3('drs.db');

$db->exec('DROP TABLE logs');

// Create logs table if not exists
$db->exec('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, time INTEGER, device TEXT, type TEXT, content TEXT)');

header('Location: /index.php');
?>