<?php
     
    require 'database.php';
 
    if ( !empty($_POST)) {
        // keep track post values
		$Firstname = $_POST['Firstname'];
		$Lastname = $_POST['Lastname'];
		$Cin = $_POST['Cin'];
        $State = $_POST['State'];
        $Temperature = $_POST['Temperature'];
		$Tension = $_POST['Tension'];
		$RFID = $_POST['RFID'];

		// insert data to rfid
		$Write = "<?php $"."obj = new stdClass(); $"."obj->Firstname = '".$Firstname."'; $"."obj->Lastname = '".$Lastname."'; $"."obj->Cin = '".$Cin."'; $"."obj->State = '".$State."'; $"."obj->Temperature = '".$Temperature."'; $"."obj->Tension = '".$Tension."'; $"."obj->RFID = '".$RFID."'; echo json_encode($"."obj); ?>";
		file_put_contents('insertData.php',$Write);
        
		
        
		// insert data to database
        $pdo = Database::connect();
		$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		$sql = "INSERT INTO healthtrackerapp_patient (Firstname,Lastname,Cin,State,Temperature,Tension,RFID) values(?, ?, ?, ?, ?, ?, ?)";
		$q = $pdo->prepare($sql);
		$q->execute(array($Firstname,$Lastname,$Cin,$State,$Temperature,$Tension,$RFID));
		Database::disconnect();
		header("Location:http://localhost:8000/Tracker/");
    }

	
?>