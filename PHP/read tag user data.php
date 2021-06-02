<?php
    require 'database.php';

    $id = null;
    if ( !empty($_GET['RFID'])) {
        $id = $_REQUEST['RFID'];
    }
     
    $pdo = Database::connect();
	$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	$sql = "SELECT * FROM healthtrackerapp_patient where RFID = ?";
	$q = $pdo->prepare($sql);
	$q->execute(array($id));
	$data = $q->fetch(PDO::FETCH_ASSOC);
	Database::disconnect();
	
	$msg = null;
	if (null==$data['Firstname']) {
		$msg = "This patient is not registered !!!";
		$data['RFID']=$id;
		$data['Firstname']="--------";
		$data['Lastname']="--------";
		$data['Cin']="--------";
		$data['State']="--------";
		$data['Temperature']="--------";
		$data['Tension']="--------";
	} else {
		$msg = null;
	}
?>
 
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
    <link   href="css/bootstrap.min.css" rel="stylesheet">
    <script src="js/bootstrap.min.js"></script>
	<style>
		td.lf {
			padding-left: 15px;
			padding-top: 12px;
			padding-bottom: 12px;
		}
	</style>
</head>
 
	<body>	
		<div>
			<form>
				<table  width="452" border="1" bordercolor="#10a0c5" align="center"  cellpadding="0" cellspacing="1"  bgcolor="#000" style="padding: 2px">
					<tr>
						<td  height="40" align="center"  bgcolor="#10a0c5"><font  color="#FFFFFF">
						<b>User Data</b></font></td>
					</tr>
					<tr>
						<td bgcolor="#f9f9f9">
							<table width="452"  border="0" align="center" cellpadding="5"  cellspacing="0">
								<tr>
									<td width="113" align="left" class="lf">ID Patient</td>
									<td style="font-weight:bold">:</td>
									<td align="left"><?php echo $data['RFID'];?></td>
								</tr>
								<tr bgcolor="#f2f2f2">
									<td align="left" class="lf">Firstname</td>
									<td style="font-weight:bold">:</td>
									<td align="left"><?php echo $data['Firstname'];?></td>
								</tr>
								<tr>
									<td align="left" class="lf">Lastname</td>
									<td style="font-weight:bold">:</td>
									<td align="left"><?php echo $data['Lastname'];?></td>
								</tr>
								<tr bgcolor="#f2f2f2">
									<td align="left" class="lf">Cin</td>
									<td style="font-weight:bold">:</td>
									<td align="left"><?php echo $data['Cin'];?></td>
								</tr>
								<tr>
									<td align="left" class="lf">Movement State</td>
									<td style="font-weight:bold">:</td>
									<td align="left"><?php echo $data['State'];?></td>
								</tr>
								<tr>
									<td align="left" class="lf">Temperature</td>
									<td style="font-weight:bold">:</td>
									<td align="left"><?php echo $data['Temperature'];?></td>
								</tr>
								<tr>
									<td align="left" class="lf">Tension</td>
									<td style="font-weight:bold">:</td>
									<td align="left"><?php echo $data['Tension'];?></td>
								</tr>
							</table>
						</td>
					</tr>
				</table>
			</form>
		</div>
		<p style="color:red;"><?php echo $msg;?></p>
	</body>
</html>