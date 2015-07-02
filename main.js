// var mraa = require('mraa'); //require mraa
// console.log('MRAA Version: ' + mraa.getVersion()); //write the mraa version to resin.io dashboard logs

// function char(x) { return parseInt(x, 16); }

// var myOnboardLed = new mraa.Gpio(5); //LED hooked up to Groove Board D5
// myOnboardLed.dir(mraa.DIR_OUT); //set the gpio direction to output
// var ledState = true; //Boolean to hold the state of Led

// periodicActivity(); //call the periodicActivity function

// function periodicActivity()
// {
//   myOnboardLed.write(ledState?1:0); //if ledState is true then write a '1' (high) otherwise write a '0' (low)
//   ledState = !ledState; //invert the ledState
//   setTimeout(periodicActivity,1000); //call the indicated function after 1 second (1000 milliseconds)
// }

// var display = require('intel-edison-lcd-rgb-backlight-display-helper');
// // Set display rows/cols
// display.set(2, 16);
// // Set color
// display.setColor('blue');
// // Display keyword on row 1
// display.write('HELLO!');

var mraa = require ('mraa');
var LCD  = require ('jsupm_i2clcd');
console.log('Current version of MRAA is', mraa.getVersion());

var lcdMessage=" ";
var myLCD = new LCD.Jhd1313m1(6, 0x3E, 0x62);

loop();

function loop(){
    lcdMessage = "Hello Hacker!";
    myLCD.setCursor(0,1);
    console.log(lcdMessage);
    myLCD.write(lcdMessage);
    setTimeout(loop,1000);
}
