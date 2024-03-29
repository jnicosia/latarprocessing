# LaTAR Bot Notes

## Pilot Phone Testing

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

| Event | Typical latency |
|-------|-----------------|
| app decides to display stimulus (dispTime) | ? |
| app displays stimulus (detectTime) | ? |
| human input response to stimulus (timestamp) |  |
| os recognizes tap (actionTime) | 5-50ms |
| app processes touch (callbackTime) | 1-5ms |

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

- display
  - no load
    - 199 ms X 100
    - 503 ms X 100
    - 997 ms X 100
  - w "Object Serialization" load (thread count = 1; min load interval = 0 ms)
    - 199 ms X 100
    - 503 ms X 100
    - 997 ms X 100
- solenoid
  - no load
    - 199 ms X 100
    - 503 ms X 100
    - 997 ms X 100
  - w "Object Serialization" load (thread count = 1; min load interval = 0 ms)
    - 199 ms X 100
    - 503 ms X 100
    - 997 ms X 100
- capacitive
  - no load
    - 199 ms X 100
    - 503 ms X 100
    - 997 ms X 100
  - w "Object Serialization" load (thread count = 1; min load interval = 0 ms)
    - 199 ms X 100
    - 503 ms X 100
    - 997 ms X 100

## To Do

- get touch sample & screen refresh rates for each phone
- recommendations to researchers: touch latency appears to be pretty consistent across phones and is within the touch sample rate (~16 ms for 60 Hz) --> in rare cases where mean differences/SDs across groups are less than touch sample rate, then phones aren't a good measurement device (but this is probably extremely rare in human behavior data collection and in remote assessments)
- show that CPU can account for tap latencies if using callback time and not action time
  - callback_latency ~ OS + geekbench_single_core vs. action_latency ~ OS + geekbench_single_core --> os/CPU should account for sig var for callback but not action

### Screen Refresh Rate

Key: While screen refresh rate defines the minimum variance a phone's screen can provide, the OS decides what the frame rate is and the developer may have options to define it. From [Apple's iOS Device Compatibility Reference](https://developer.apple.com/library/archive/documentation/DeviceInformation/Reference/iOSDeviceCompatibility/Displays/Displays.html):

    Under most circumstances, UIKit handles redrawing and animation for you, adjusting the frame rate as necessary to provide a good viewing experience with reasonable energy usage. However, when you configure a view animation, you can optionally specify a hint when you know that the animation should run at a higher or lower rate. For more information, see UIViewAnimationOptions.

# Sources used for phone_data.csv

- Geekbench 5 CPU workloads documentation: https://www.geekbench.com/doc/geekbench5-cpu-workloads.pdf
- Apple documentation on display refresh and touch sampling rates: 1
- Some Samsung info in screen refresh rate: https://www.samsung.com/us/support/answer/ANS00086005/
