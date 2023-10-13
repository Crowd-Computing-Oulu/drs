<!DOCTYPE html>
<html>

<head>
  <title>PHP Database Test</title>
</head>

<body>
  <h1>PHP Database Test</h1>

  <?php
  $db = new PDO('sqlite:/web-db/test.db');
  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

  try {
    $query = "CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, name TEXT)";
    $db->exec($query);

    $name = "John Doe";
    $stmt = $db->prepare("INSERT INTO test_table (name) VALUES (:name)");
    $stmt->bindParam(':name', $name);
    $stmt->execute();

    echo "Table 'test_table' created, and a record added successfully.";
  } catch (PDOException $e) {
    echo "Error: " . $e->getMessage();
  }
  ?>

  <p>Check the database to see if the table and record were created.</p>
</body>

</html>