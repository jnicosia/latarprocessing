# LaTAR Bot Notes

## Phone Testing

### Samsung SM-A305G

- [x] capacitive
- [x] display
- [x] solenoid

### Samsung SM-G960U (Ben's S9)

- [x] capacitive
- [x] display
- [x] solenoid

### Motorola moto g stylus

- [x] capacitive
- [x] display
- [x] solenoid

### Samsung SM-A125M

- [ ] capacitive
- [x] display
- [x] solenoid

### Samsung SM-A525M

- [x] capacitive
- [x] display
- [x] solenoid

### iPhone 11

- [x] capacitive
- [x] display
- [x] solenoid

### iPhone XR

- [x] capacitive
- [x] display
- [x] solenoid

### iPhone XS

- [x] capacitive
- [x] display
- [x] solenoid

### iPhone 7

- [x] capacitive
- [x] display
- [x] solenoid

### iPhone 8

- [x] capacitive
- [x] display
- [x] solenoid

### iPhone X

- [x] capacitive
- [x] display
- [x] solenoid

### Samsung SM-A515F

- [ ] capacitive
- [x] display
- [x] solenoid

### Samsung SM-A5325M

- [x] capacitive
- [x] display
- [x] solenoid

### Samsung SM-A102U

- [ ] capacitive
- [x] display
- [x] solenoid

### Samsung SM-S111DL

- [x] capacitive
- [x] display
- [x] solenoid

### moto e

- unable to get past activation

### nokia 2 v tella

- unable to get past activation

### Wiko Ride 3

- [x] capacitive
- [x] display
- [ ] solenoid

### LG Journey

- [x] capacitive
- [x] display
- [x] solenoid

## Event Timeline

1. app decides to display stimulus (dispTime)
2. app displays stimulus (detectTime)
3. human input response to stimulus (timestamp)
4. os recognizes tap (actionTime)
5. app processes touch (callbackTime)

## Procedure(s)

### Pilot

- capacitive
  - no load
    - 500 ms X 50
- display
  - no load
    - 500 ms X 50
- solenoid
  - no load
    - 500 ms X 50

### Experimental

- capacitive
  - no load
    - 500 ms X 200
    - 300 ms X 200
    - 100 ms X 200
  - w load (decide which option)
    - 500 ms X 200
    - 300 ms X 200
    - 100 ms X 200
- display
  - no load
    - 500 ms X 200
    - 300 ms X 200
    - 100 ms X 200
  - w load (decide which option)
    - 500 ms X 200
    - 300 ms X 200
    - 100 ms X 200
- solenoid
  - no load
    - 500 ms X 200
    - 300 ms X 200
    - 100 ms X 200
  - w load (decide which option)
    - 500 ms X 200
    - 300 ms X 200
    - 100 ms X 200
    
## Misc. Notes

- try using prime number for ITI (i.e., instead of 500 ms --> 499/503) to help reduce any touch screen sampling rate
- get touch sample & screen refresh rates for each phone
- get measure of phone performance. Options:
  - Worst: CPU frequency for each phone (?). Doesn't factor in other aspects of phone performance.
  - Better: Get benchmark results available online (eg., Geekbench 5 or 3D Mark). Not available for all phones and is model-specific
  - Best: Run benchmark on actual phones
- recommendations to researchers: touch latency appears to be pretty consistent across phones and is within the touch sample rate (~16 ms for 60 Hz) --> in rare cases where mean differences/SDs across groups are less than touch sample rate, then phones aren't a good measurement device (but this is probably extremely rare in human behavior data collection and in remote assessments)
- show that CPU can account for tap latencies if using callback time and not action time
- can we get the code for the phone apps? Better understanding of what's going on

### Screen Refresh Rate

Key: While screen refresh rate defines the minimum variance a phone's screen can provide, the OS decides what the frame rate is and the developer may have options to define it. From [Apple's iOS Device Compatibility Reference](https://developer.apple.com/library/archive/documentation/DeviceInformation/Reference/iOSDeviceCompatibility/Displays/Displays.html):

    Under most circumstances, UIKit handles redrawing and animation for you, adjusting the frame rate as necessary to provide a good viewing experience with reasonable energy usage. However, when you configure a view animation, you can optionally specify a hint when you know that the animation should run at a higher or lower rate. For more information, see UIViewAnimationOptions.

# Sources used for phone_data.csv

- Apple documentation on display refresh and touch sampling rates: https://developer.apple.com/library/archive/documentation/DeviceInformation/Reference/iOSDeviceCompatibility/Displays/Displays.html
- Some Samsung info in screen refresh rate: https://www.samsung.com/us/support/answer/ANS00086005/
