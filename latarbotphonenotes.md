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

### iPhone X (Jessica's iPhone)

- [x] capacitive
- [x] display
- [ ] solenoid

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
