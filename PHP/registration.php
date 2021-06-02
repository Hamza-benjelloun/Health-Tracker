<?php
	$Write="<?php $" . "UIDresult=''; " . "echo $" . "UIDresult;" . " ?>";
	file_put_contents('UIDContainer.php',$Write);
?>

<!DOCTYPE html>
<html lang="en">
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta charset="utf-8">
		<link href="css/bootstrap.min.css" rel="stylesheet">
		<script src="js/bootstrap.min.js"></script>
		<script src="jquery.min.js"></script>
		<script>
			$(document).ready(function(){
				 $("#getUID").load("UIDContainer.php");
				setInterval(function() {
					$("#getUID").load("UIDContainer.php");
				}, 500);
			});
		</script>
		
		<style>
		
		html {
			font-family: Arial;
			display: inline-block;
			margin: 0px auto;
		}
		
		textarea {
			resize: none;
		}

		ul.topnav {
			list-style-type: none;
			margin: auto;
			padding: 0;
			overflow: hidden;
			background-color: #3c5975;
			width: 70%;
		}

		ul.topnav li {float: left;}

		ul.topnav li a {
			display: block;
			color: white;
			text-align: center;
			padding: 14px 16px;
			text-decoration: none;
		}

		ul.topnav li a:hover:not(.active) {background-color: #3e8e41;}

		ul.topnav li a.active {background-color: #333;}

		ul.topnav li.right {float: right;}

		@media screen and (max-width: 600px) {
			ul.topnav li.right, 
			ul.topnav li {float: none;}
		}
		body{
			background: url('/img/HealthtrackerBg.png');
			background-repeat: no-repeat;
			background-size: 100% 700px;
			overflow: hidden;
		}
		</style>
		
		<title>Add</title>
	</head>
	
	<body style="background: url('img/HealthtrackerBg.png');
			background-repeat: no-repeat;
			background-size: 100% 700px;
			overflow: hidden;">

		<ul class="topnav">
			<li><a href="http://localhost:8000/Tracker/">Home</a></li>
			<li><a class="active" href="registration.php">Registration</a></li>
			<li><a href="read tag.php">Read Tag ID</a></li>
		</ul>

		<div class="container">
			<br>
			<div class="center" style="color:#cbe3f1;margin: 0 auto; width:495px; border-style: solid; border-color: #f2f2f2; background-color:rgba(0, 0, 0, 0.493);">
				<div class="row">
					<h3 align="center">Registration Form</h3>
				</div>
				<br>
				<form class="form-horizontal" action="insertDB.php" method="post" >
					<div class="control-group">
						<label class="control-label">ID Patient</label>
						<div class="controls">
							<textarea name="RFID" id="getUID" placeholder="Please Scan your Card / Key Chain to display ID" rows="1" cols="1" required></textarea>
						</div>
					</div>
					
					<div class="control-group">
						<label class="control-label">Firstname</label>
						<div class="controls">
							<input id="div_refresh" name="Firstname" type="text"  placeholder="" required>
						</div>
					</div>
					
					<div class="control-group">
						<label class="control-label">Lastname</label>
						<div class="controls">
							<input name="Lastname" type="text"  placeholder="" required>
						</div>
					</div>
					
					<div class="control-group">
						<label class="control-label">Cin</label>
						<div class="controls">
							<input name="Cin" type="text"  placeholder="" required>
						</div>
					</div>
					
					<div class="control-group">
						<label class="control-label">Movement State</label>
						<div class="controls">
							<input name="State" type="text"  placeholder="">
						</div>
					</div>

					<div class="control-group">
						<label class="control-label">Temperature</label>
						<div class="controls">
							<input name="Temperature" type="text"  placeholder="">
						</div>
					</div>

					<div class="control-group">
						<label class="control-label">Tension</label>
						<div class="controls">
							<input name="Tension" type="text"  placeholder="">
						</div>
					</div>
					
					<div class="form-actions" style="background-color:rgba(0, 0, 0, 0);">
						<button type="submit" class="btn btn-success">Save</button>
                    </div>
				</form>
				
			</div>               
		</div> <!-- /container -->	
	</body>
</html>