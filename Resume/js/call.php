<?php
    $xmldoc=new DOMDocument("1.0","utf-8");
    $xmldoc->formatOutput=true;
    $xmldoc->load("data.xml");
    $messages=$xmldoc->getElementsByTagName("messages")->item(0);

   $message=$xmldoc->createElement("message");

   $name=$xmldoc->createElement("name");
   $name->nodeValue=$_GET['fullname'];
   $message->appendChild($name);

   $phone=$xmldoc->createElement("phone");
   $phone->nodeValue=$_GET['phone'];
   $message->appendChild($phone);

   $msg=$xmldoc->createElement("msg");
   $msg->nodeValue=$_GET['message'];
   $message->appendChild($msg);

   $messages->appendChild($message);
   $xmldoc->save("data.xml");
   
   echo "廖志明已经收到您宝贵的建议啦!";
   ?>

   