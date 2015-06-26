var mraa = require('mraa'); //require mraa
console.log('MRAA Version: ' + mraa.getVersion()); //write the mraa version to resin.io dashboard logs

function char(x) { return parseInt(x, 16); }

var myOnboardLed = new mraa.Gpio(5); //LED hooked up to Groove Board D5
myOnboardLed.dir(mraa.DIR_OUT); //set the gpio direction to output
var ledState = true; //Boolean to hold the state of Led

periodicActivity(); //call the periodicActivity function

function periodicActivity()
{
  myOnboardLed.write(ledState?1:0); //if ledState is true then write a '1' (high) otherwise write a '0' (low)
  ledState = !ledState; //invert the ledState
  setTimeout(periodicActivity,1000); //call the indicated function after 1 second (1000 milliseconds)
}

var display = require('intel-edison-lcd-rgb-backlight-display-helper');
// Set display rows/cols
display.set(2, 16);
// Set color
display.setColor('blue');
// Display keyword on row 1
display.write('HELLO!');

// From https://github.com/intel-iot-devkit/mraa/blob/v0.7.2/examples/javascript/rgblcd.js
// lcd = new mraa.I2c(0)

// lcd.address(0x62)
// lcd.writeReg(0, 0)
// lcd.writeReg(1, 0)

// lcd.writeReg(char('0x08'), char('0x88'))
// lcd.writeReg(char('0x04'), 255)
// lcd.writeReg(char('0x02'), 255)

// periodicActivity();

// ledval = 97

// function periodicLCDActivity()
// {
//     lcd.write(char('0x40'), ledval)
//     console.log(ledval);
//     ledval++;
//     if (ledval > 126) {
// 	ledval = 97;
//     }
//     setTimeout(periodicLCDActivity,1000); //call the indicated function after 1 second (1000 milliseconds)
// }
