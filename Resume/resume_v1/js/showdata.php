
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
        $message=$messages->item($i);

        echo $message->getElementsByTagName("name")->item(0)->nodeValue;
        echo $message->getElementsByTagName("phone")->item(0)->nodeValue;
        echo $message->getElementsByTagName("msg")->item(0)->nodeValue;
    }
}else
    echo "暂无数据！";
