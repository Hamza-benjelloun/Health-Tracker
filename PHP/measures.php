<?php
    //Connect to database
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "healthtracker";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    // Check connection
    if ($conn->connect_error) {
        die("Database Connection failed: " . $conn->connect_error);
    }
    if( !empty($_POST['id_patient']) && !empty($_POST['temperature']) && !empty($_POST['temp_state']) && !empty($_POST['tension']) && !empty($_POST['tension_state']))
    {
        $id_patient = $_POST['id_patient'];
        $temperature = $_POST['temperature'];
        $temp_state = $_POST['temp_state'];
        $tension = $_POST['tension'];
        $tension_state = $_POST['tension_state'];

        $sql = "INSERT INTO healthtrackerapp_measures (id_patient,temperature,temp_state,tension,tension_state) VALUES ('".$id_patient."','".$temperature."','".$temp_state."','".$tension."','".$tension_state."')";
        if ($conn->query($sql) === TRUE) {
            echo "DONE!";
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    }
    else
        echo "Error!";
    $conn->close();
?>