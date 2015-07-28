var mraa = require ('mraa');
console.log('Current version of MRAA is', mraa.getVersion());
var display = require('intel-edison-lcd-rgb-backlight-display-helper');

// Set display rows/cols
display.set(2, 16);

// Set color
display.setColor('red');

// If you want to update only row 2
display.write([null, 'OH MY!']);
