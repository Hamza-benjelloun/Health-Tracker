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

     
     if( !empty($_POST['id_patient']) )
    {
        $id_patient = $_POST['id_patient'];

        $sql = "SELECT * FROM healthtrackerapp_patient WHERE RFID='".$id_patient."'";

        $result = mysqli_query($conn,$sql);
        $found = false;

        while($row = mysqli_fetch_assoc($result))
            {echo $row['Firstname'];
            $found = true;
            }

        if ($found == false)
            echo "None";
    }
    else
        echo "Error!";

    $conn->close();
    
?>