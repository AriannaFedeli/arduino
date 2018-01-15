<?php

/**
 * This is a reader of Arduino's generated data. 
 * The reader will read data and then send via post request.
 * 
 */

include dirname(__FILE__).'/PhpSerial.php';

// Let's start the class
$serial = new PhpSerial;

// First we must specify the device. This works on both linux and windows (if
// your linux serial device is /dev/ttyS0 for COM1, etc)
$serial->deviceSet("/dev/ttyACM0");

// Then we need to open it
$serial->deviceOpen();

echo $serial->readPort();


