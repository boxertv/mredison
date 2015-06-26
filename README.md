# edison-blink-node

A simple node.js project to get you started with the [Intel Edison][edison-link] and [Resin.io][resin-link].
This project uses the [MRAA][mraa-repo] library to toggle the onboard led (GPIO 13) of the [Intel Edison arduino][edison-arduino-board] base board on and off.


To get this project running on your intel edison, first checkout the ["Getting Started with Intel Edison"][getting-started page in the docs..

If you already have a resin.io account:
* Create a new Intel Edison project 
* add/provision as many edisons as you want to the app, if you need help doing this check [here][provision-an-edison].
* Clone this repo to your development computer and add your you resin.io applications endpoint, it should look something like `git@git.resin.io:shaunrmulligan/myedison.git`
* Now run `git push resin master` from the newly cloned project.
* After the code has compiled and been downloaded by the device(s), you should have some leds happily blinking away.

Enjoy!!

[edison-link]:http://www.intel.com/content/www/us/en/do-it-yourself/edison.html
[edison-arduino-board]:https://www.sparkfun.com/products/13097
[resin-link]:https://resin.io/
[mraa-repo]:https://github.com/intel-iot-devkit/mraa
[getting-started]:http://docs.resin.io/#/pages/installing/getting-started-edison.md
[signup-link]:https://dashboard.resin.io/signup
[provison-an-edison]:http://docs.resin.io/#/pages/installing/getting-started-edison.md#adding-your-first-edison-device
