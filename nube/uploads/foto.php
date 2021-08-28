<?php
/*
	Tomar foto con Python y opencv para después mandarla
	a un servidor PHP
	@date 20-03-2018
	@author parzibyte
	@see https://www.parzibyte.me/blog
*/
isset($_POST["foto"]) || exit();
$bytes = file_put_contents(uniqid() . ".jpg", base64_decode($_POST["foto"]));
echo json_encode($bytes);
?>
