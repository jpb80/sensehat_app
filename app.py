#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sense_hat
import logging as _log
import datetime
import time


def _logger_config():
    _log.basicConfig(level=_log.INFO, format=("[###%(levelname)s] "
                                                    "%(asctime)s: "
                                                    "%(filename)s: "
                                                    "%(funcName)s(): "
                                                    "%(lineno)d: "
                                                    "%(message)s"))
    _log.info("Started")


def _convert_to_farenheit(celsius):
    return celsius * 5 / 9 + 32


def _determine_temp_led_color(temp_fahrenheit):
    result = [255, 0, 250]
    if temp_fahrenheit >= 95:
        result = [255, 0 , 0]
    elif temp_fahrenheit >= 80 and temp_fahrenheit < 95:
        result = [255, 93, 0]
    elif temp_fahrenheit >= 76 and temp_fahrenheit < 80:
        result = [255, 233, 0]
    elif temp_fahrenheit >= 70 and temp_fahrenheit < 76:
        result = [118, 255, 0]
    elif temp_fahrenheit >= 55 and temp_fahrenheit < 70:
        result = [0, 255, 137]
    elif temp_fahrenheit >= 40 and temp_fahrenheit < 55:
        result = [0, 208, 255]
    elif temp_fahrenheit >= 33 and temp_fahrenheit < 40:
        result = [0, 110, 255]
    elif temp_fahrenheit >= 20 and temp_fahrenheit < 32:
        result = [0, 29, 255]
    elif temp_fahrenheit >= 0 and temp_fahrenheit < 20:
        result = [51, 0, 255]
    return result


def _get_local_time():
    return datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")


def main():
    _logger_config()
    sense = sense_hat.SenseHat()

    while True:
        event = sense.stick.wait_for_event(emptybuffer=True)
        if event.action == stick.ACTION_PRESSED:
            if event.direction == stick.DIRECTION_MIDDLE:
                sense.show_message(_get_local_time(), text_colour=[255,0,255])
            elif event.direction == stick.DIRECTION_UP:
                sense.show_message("{0:.1f} %%rH".format(humidity),
                                   text_colour=[255,0,255])
            elif event.direction == stick.DIRECTION_DOWN:
                sense.show_message("{0:.1f} °F".format(curr_temp),
                                   text_colour=_determine_temp_led_color(curr_temp))
            elif event.direction == stick.DIRECTION_LEFT:
                sense.show_message("{0:.3f} mbar".format(curr_pressure),
                                text_colour=[255,0,255])
        while event is not None:
            north = sense.get_compass()
            print("{0:.1f}°N".format(north))

            humidity = sense.get_humidity()
            print("{0:.1f} %%rH".format(humidity))

            curr_temp = _convert_to_farenheit(sense.get_temperature_from_humidity())
            print("{0:.1f}°F".format(curr_temp))

            curr_pressure = sense.get_pressure()
            print("{0:.4f} Millibars".format(curr_pressure))
            time.sleep(2)


if __name__ == '__main__':
    main()
