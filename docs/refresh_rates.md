# Refresh Rates

## Android
### Touch sampling rate

1. Connect to phone via USB
2. Open terminal with adb, run: `adb devices`
    a. If you get "unauthorized", make sure to enable developer mode on the phone and then allow USB debugging for the connected PC
	

You should see something like the following:

```
ben@Tucana-Ubuntu:~$ adb devices
List of devices attached
01AAY1SSP9 unauthorized


ben@Tucana-Ubuntu:~$ adb devices
List of devices attached
01AAY1SSP9 device


ben@Tucana-Ubuntu:~$ adb shell getevent -r -t -l

...

[   91129.508444] /dev/input/event2: EV_SYN       SYN_REPORT           00000000             rate 114
[   91129.516917] /dev/input/event2: EV_ABS       ABS_MT_POSITION_X    00000281            
[   91129.516917] /dev/input/event2: EV_ABS       ABS_MT_POSITION_Y    00000467            
[   91129.516917] /dev/input/event2: EV_SYN       SYN_REPORT           00000000             rate 118
[   91129.525672] /dev/input/event2: EV_ABS       ABS_MT_POSITION_X    00000278            
[   91129.525672] /dev/input/event2: EV_ABS       ABS_MT_POSITION_Y    0000046e            
[   91129.525672] /dev/input/event2: EV_SYN       SYN_REPORT           00000000             rate 114
[   91129.534141] /dev/input/event2: EV_ABS       ABS_MT_POSITION_X    00000270            
[   91129.534141] /dev/input/event2: EV_ABS       ABS_MT_POSITION_Y    00000475            
[   91129.534141] /dev/input/event2: EV_SYN       SYN_REPORT           00000000             rate 118

```

### Screen refresh rate

1. Connect to phone via ADB (see above)
2. Run  `adb shell dumpsys display | grep fps`

You should get something like this (Pixel 3a):

```
ben@Tucana-Ubuntu:~$ adb shell dumpsys display | grep fps
  DisplayDeviceInfo{"Built-in Screen": uniqueId="local:0", 1080 x 2220, modeId 1, defaultModeId 1, supportedModes [{id=1, width=1080, height=2220, fps=60.000004}], colorMode 0, supportedColorModes [0, 7], HdrCapabilities HdrCapabilities{mSupportedHdrTypes=[2, 3], mMaxLuminance=500.0, mMaxAverageLuminance=500.0, mMinLuminance=0.0}, allmSupported false, gameContentTypeSupported false, density 440, 442.451 x 444.0 dpi, appVsyncOff 2000000, presDeadline 11666666, touch INTERNAL, rotation 0, type INTERNAL, address {port=0}, deviceProductInfo null, state OFF, FLAG_DEFAULT_DISPLAY, FLAG_ROTATES_WITH_CONTENT, FLAG_SECURE, FLAG_SUPPORTS_PROTECTED_BUFFERS}
      DisplayModeRecord{mMode={id=1, width=1080, height=2220, fps=60.000004}}
    mBaseDisplayInfo=DisplayInfo{"Built-in Screen", displayId 0, FLAG_SECURE, FLAG_SUPPORTS_PROTECTED_BUFFERS, FLAG_TRUSTED, real 1080 x 2220, largest app 1080 x 2220, smallest app 1080 x 2220, appVsyncOff 2000000, presDeadline 11666666, mode 1, defaultMode 1, modes [{id=1, width=1080, height=2220, fps=60.000004}], hdrCapabilities HdrCapabilities{mSupportedHdrTypes=[2, 3], mMaxLuminance=500.0, mMaxAverageLuminance=500.0, mMinLuminance=0.0}, minimalPostProcessingSupported false, rotation 0, state OFF, type INTERNAL, uniqueId "local:0", app 1080 x 2220, density 440 (442.451 x 444.0) dpi, layerStack 0, colorMode 0, supportedColorModes [0, 7], address {port=0}, deviceProductInfo null, removeMode 0}
    mOverrideDisplayInfo=DisplayInfo{"Built-in Screen", displayId 0, FLAG_SECURE, FLAG_SUPPORTS_PROTECTED_BUFFERS, FLAG_TRUSTED, real 1080 x 2220, largest app 2088 x 2022, smallest app 1080 x 1014, appVsyncOff 2000000, presDeadline 11666666, mode 1, defaultMode 1, modes [{id=1, width=1080, height=2220, fps=60.000004}], hdrCapabilities HdrCapabilities{mSupportedHdrTypes=[2, 3], mMaxLuminance=500.0, mMaxAverageLuminance=500.0, mMinLuminance=0.0}, minimalPostProcessingSupported false, rotation 0, state ON, type INTERNAL, uniqueId "local:0", app 1080 x 2088, density 440 (442.451 x 444.0) dpi, layerStack 0, colorMode 0, supportedColorModes [0, 7], address {port=0}, deviceProductInfo null, removeMode 0}
    0 -> [{id=1, width=1080, height=2220, fps=60.000004}]
    0 -> {id=1, width=1080, height=2220, fps=60.000004}
```

## References

- Identify touch sampling rate on android: Tutorial: How to check touch sampling rate on Android phones | S20+ only 120Hz? Redmi Note 9 Pro?
- Get android refresh rate: https://android.stackexchange.com/questions/106554/how-can-i-get-the-refresh-rate-via-adb#:~:text=You%20can%20get%20the%20refresh%20rate%20through%20this,too.%20Derived%20from%20chr0m4k3y%27s%20answer%20on%20Stack%20Overflow.
    - Also: https://stackoverflow.com/questions/60374594/how-to-change-refresh-rate-by-adb-command