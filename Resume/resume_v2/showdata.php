<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="shortcut icon" type="image/x-icon" href="images/logo.ico" media="screen"/>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>廖志明个人简历</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1 class="lead">简历留言</h1>
    <table class="table table-hover table-border table-striped">    
<?php
/**
 * Created by PhpStorm.
 * User: Andy Liao
 * Date: 2018-03-03
 * Time: 19:49
 */
$xmldoc=new DOMDocument();
$xmldoc->load("data.xml");

$messages=$xmldoc->getElementsByTagName("message");

if($messages->length>0){
    for($i=0;$i<$messages->length;$i++){
        if($i%5==0)
        echo '<tr class="active">';
        else{
            if($i%5==1)
                echo '<tr class="success">';
            else{
                if($i%5==2){
                    echo '<tr class="danger">';
                }
            else{
            echo '<tr class="info">';}
        }
    }
        echo "<td>";
        if($i==0)
            echo "No";
        else
            echo $i;
        echo "</td>";
        $message=$messages->item($i);

        echo "<td>";
        echo $message->getElementsByTagName("name")->item(0)->nodeValue;
         echo "</td>";
        echo "<td>";
        echo $message->getElementsByTagName("phone")->item(0)->nodeValue;
         echo "</td>";
        echo "<td>";
        echo $message->getElementsByTagName("msg")->item(0)->nodeValue;
        echo "</td>";
        echo "</tr>";
    }
}else
    echo "暂无数据！";
    ?>
    </table>
    </div>
    </body>
</html>