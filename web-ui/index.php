<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

$db = new SQLite3('drs.db');

// Create instructions table if not exists
$db->exec('CREATE TABLE IF NOT EXISTS instructions (id INTEGER PRIMARY KEY, time INTEGER, device TEXT, instruction TEXT, params TEXT)');

// Create logs table if not exists
$db->exec('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, time INTEGER, device TEXT, type TEXT, content TEXT)');


$logs = [];
$result = $db->query('SELECT * FROM logs ORDER BY time DESC');
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $logs[] = $row;
}

$instructions = [];
$result = $db->query('SELECT * FROM instructions');
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $instructions[] = $row;
}

# hard-coded for now
$devices = [
  [
    'id' => 0,
    'name' => "Pepper Robot",
  ],
  [
    'id' => 1,
    'name' => "Apple Watch",
  ]
];

// some that are supposed to be supported
//  - transfer_conv_from
//  - transfer_conv_to
//  - shut_down
//  - restart
//  - reset_conv
//  - say
// $instructions = [
  // example instruction 1
  // [
  //   'device' => "0", (the device that the instruction is addressed to)
  //   'instruction' => "transfer_conv_to", (the instruction itself)
  //   'params' => "",
  // ]
  // example instruction 2
  // [
  //   'device' => "1", 
  //   'instruction' => "say", 
  //   'params' => "Hello from DRS!",
  // ]
// ];

// handle incoming messages
if (isset($_POST['message'])) {
  switch ($_POST['message']){
    case "transfer_conv_from":
      $instructions[] = [
        'device' => "1",  // addressed to 1, arrived from 0
        'time'=> time(),
        // 'instruction' => $_POST['message'], 
        'instruction' => "transfer_conv_to",
        'params' => $_POST['params'],
      ];
      $statement = $db->prepare('INSERT INTO instructions (time, device, instruction, params) VALUES (:time, :device, :instruction, :params)');
      $statement->bindValue(':time', time(), SQLITE3_INTEGER);
      $statement->bindValue(':device', 1, SQLITE3_INTEGER);
      $statement->bindValue(':instruction', "transfer_conv_to", SQLITE3_TEXT);
      $statement->bindValue(':params', $_POST["params"], SQLITE3_TEXT);
      $statement->execute();
      header('Location: /index.php');
      break;
  }
  exit();
}

// handle incoming log
if (isset($_POST["log"])) {
  $logs[] = [
    'time'=>time(),
    'device'=>$_POST["device"],
    'content'=>$_POST["content"],
    'type'=>$_POST["type"],
  ];
  $statement = $db->prepare('INSERT INTO logs (time, device, type, content) VALUES (:time, :device, :type, :content)');
  $statement->bindValue(':time', time(), SQLITE3_INTEGER);
  $statement->bindValue(':device', $_POST["device"], SQLITE3_INTEGER);
  $statement->bindValue(':content', $_POST["content"], SQLITE3_TEXT);
  $statement->bindValue(':type', $_POST["type"], SQLITE3_TEXT);
  $statement->execute();
  header('Location: /index.php');
  exit();
} else {
  // var_dump($_POST);
}
?>

<!DOCTYPE html>
<html>

<head>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php
    $page = $_SERVER['PHP_SELF'];
    $sec = "2.5";
    ?>
    <meta http-equiv="refresh" content="<?php echo $sec?>;URL='<?php echo $page?>'">
    <title>DRS Admin Panel</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css">
  </head>
</head>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DRS Admin Panel</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body>
<nav class="navbar navbar-expand-lg navbar-primary bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">DRS Admin Panel</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNavDropdown">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="https://github.com/Crowd-Computing-Oulu/drs">DRS on GitHub</a>
        </li>
      </ul>
    </div>
  </div>
</nav>

  <section class="section">
    <div class="container">
      <h2 class="subtitle">
        Instructions
      </h2>

      <div class="btn-toolbar" role="toolbar">
        <form class="me-2" action="/reset_instructions.php" method="GET">
          <button class="btn btn-primary" type="submit">Clear instructions</button>
        </form>

        <form action="/index.php" method="POST">
          <input type="hidden" name="message" value="transfer_conv_from">
          <input type="hidden" name="params" value="">
          <button class="btn btn-primary" type="submit">Send 'transfer_conv_from'</button>
        </form>
      </div>

      <table class="table" id="instructions_table">
        <thead>
          <tr>
            <th>Time</th>
            <th>Device</th>
            <th>Type</th>
            <th>Content</th>
          </tr>
        </thead>
        <tbody>
          <?php foreach ($instructions as $instruction): ?>
          <tr>
            <td><?php echo date('Y-m-d H:i:s', $instruction['time']); ?></td>
            <td><?php echo $instruction['device']; ?></td>
            <td><?php echo $instruction['instruction']; ?></td>
            <td><?php echo $instruction['params']; ?></td>
          </tr>
          <?php endforeach; ?>
        </tbody>
      </table>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2 class="subtitle">
        Logs
      </h2>
      <div class="btn-toolbar" role="toolbar">
        <form action="/resetdb.php" method="GET">
          <button class="btn btn-primary" type="submit">Clear log</button>
        </form>
      </div>
      <table class="table" id="logs_table">
        <thead>
          <tr>
            <th>Time</th>
            <th>Device</th>
            <th>Type</th>
            <th>Content</th>
          </tr>
        </thead>
        <tbody>
          <?php foreach ($logs as $log): ?>
          <tr>
            <td><?php echo date('Y-m-d H:i:s', $log['time']); ?></td>
            <td><?php echo $log['device']; ?></td>
            <td><?php echo $log['type']; ?></td>
            <td><?php echo $log['content']; ?></td>
          </tr>
          <?php endforeach; ?>
        </tbody>
      </table>
    </div>
  </section>

</body>

</html>
