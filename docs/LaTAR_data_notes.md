General Information
-------------------

This document aims to describe the contents of the json exported from the LaTAR server.

Before we dive into that, here's a brief description of some of the names used:
- An Objective is defined as a single test type, and its parameters (ie a screen latency 
  test, running 20 iterations at 500 ms intervals)
- A Procedure is a predefined set of Objectives -- you could, for instance, setup a 
  Procedure than runs through multiple tap latency tests at varying intervals
  
- A Session refers to a specific run of a Procedure, and the data collected (this is essentially what is being exported)


The json export contains several parts, which will be explained in more detail below. 
Each export should contain:

- id		(an id number)
- startTime	(date/time of when the session began)
- stopTime	(date/time of when the session ended)
- clockSync	(data on synchronizing clocks, more info below)
- fixture	(information about the LaTAR device)
- mobile	(information about the mobile device)
- procedure	
- objectives (data collected for each test, more info below)
- results


Entries for 'fixture' and 'mobile' contain information about the devices. The mobile device will return information about the app version, os version, and hardware details. The LaTAR device similarly returns some basic information. In the event that we have more revisions, this would be used to differentiate what version device the data was generated.

The 'procedure' entry contains the test parameters for each Objective.  For tap latency and screen latency tests, it lists the number of iterations, and the time interval between iterations.

The 'results' entry currently only contains a list of objectives and their type. 


Clock Sync Data
---------------

This data is used to synchronize the clocks between the server, mobile device, and fixture. Offset values are calculated for the mobile and the fixture, which are then applied to the collected data to bring the timestamps from both devices into the same frame of reference.

Data points collected for Clock Sync:

 - t0			(a unix timestamp in microseconds, noting the time that the server issued the initial clock sync signal)
 - t1			(a unix timestamp in microseconds, of when the initial clock sync signal is finished)
 - roundTrips	(an array, each item representing one request from the server to the mobile device for its current timestamp)
   - localSend	(server timestamp in microseconds of immediately before the message is sent)
   - localRecv	(server timestamp in microseconds of when the reply is received)
   - remote		(mobile timestamp in microseconds of when the mobile device received the request)
   
Several other values are included, which are calculated from the above data:
- offset		(value in microseconds offset between the mobile device's time and the server's time)
- avgTcs		(value in microseconds, the average duration of the requests)
- stdDevTcs		(standard deviation of the request durations)


Where localSend, localRecv, and remote are values relative to t0.

The offset values are calculated based on an implementation of the Network Time Protocol clock synchronization algorithm ( https://en.wikipedia.org/wiki/Network_Time_Protocol#Clock_synchronization_algorithm )

For each item in roundTrips, we first find the total transmission delay (the amount of time spent while data is in transmission). Our algorithm assumes that the time between when the client receives the request and when it responds is negligible, so the delay is simply:

delay = localRecv - localSend

The total transmission delay is assumed to be symmetrical, or in other words, that the delay between the server sending and the client receiving is equal to the delay between the client sending and the server receiving. Making this assumption, we can then calculate the difference between the two devices' clocks:

Tcs = (localSend + ( delay / 2)) - remote

Then we find the average (avgTcs) and standard deviation (stdDevTcs) of Tcs from each trip. And, finally, take the average of Tcs from each trip, discarding any values that are +/- 2*stdDevTcs, resulting in our estimated clock offset.

To transform a client timestamp to server time, we calculate:

corrected time = remote + t0 - offset


Objectives
----------

An Objective represents all of the parameters, collected data, and results, of test. A procedure can potentially contain multiple Objectives, if, for instance, you ran both the tap latency and screen latency tests in one run.

For both Display Latency and Tap Latency, the available parameters are:
- count		(the number of times to perform the given action)
- interval	(the amount of time in milliseconds between each action)


Data points collected for Display Latency:

* From mobile:
  - index		(0-based index, the current iteration of the action)
  - callbackTime (device timestamp in microseconds immediately before the operation to change device color is called)
  
  - displayTime	(device timestamp in microseconds immediately after the operation to change device color has finished )

  - color		(0/1 value, where 0 = black, 1 = white. This is the color that the screen was changed to)
  - colorName	(string value, either "BLACK" or "WHITE")
  
* From fixture:
 - index		(0-based index, the current iteration of the action)
 - detectTime	(device timestamp in microseconds of when the fixture detects a color change)
 - value		(string value, either "DARK" or "LIGHT", the color that was detected)
 
 
 Data points collected for Tap Latency:
 
 * From mobile:
  - index		(0-based index, the current iteration of the action)
  - action		(0/1 value, where 0 = touch down detected, 1 = touch up detected)
  - actionName	(string value, either "ACTION_DOWN" or "ACTION_UP")
  - actionTime	(device timestamp in microseconds, the timestamp recorded by OS of when the event happened)
  - callbackTime (device timestamp in microseconds recorded when the event is received by the application code)
  - touchMajor	(major diameter of the recorded touch)
  - touchMinor	(minor diameter of the recorded touch)
  
* From fixture:
 - index		(0-based index, the current iteration of the action)
 - timestamp	(device timestamp in microseconds of when the touch action was fired)
 

==========
 
A brief clarification about the touchMajor and touchMinor value:
 
Both iOS and Android provide some level of detail about the size of the touch detected, though, as with many things, they do so in different ways. Android provides two values, a "touchMajor" and "touchMinor" value, which represent the major and minor diameters of an ellipse that best fits the detected touch. iOS, on the other hand, only provides a single value, a "touchRadius" value, which we then double and set for both touchMajor and touchMinor fields. 

In each case, these values are in pixel or point units, and don't immediately represent a real-world measurement.


==========

An explanation of the differences between callbackTime and actionTime

In iOS and Android, touch events are handled in roughly the same way:
- Something (ie a finger) touches the screen (or moves on the screen, or is lifted from the screen)
- The change in touch is detected, and a lower-level framework (ie UIKit for iOS) generates an event object, which provides all of the information about the touch (ie a UITouch object)
- The framework then notifies the application by calling the appropriate method (ie touchesBegan)
- The application handles the touch

The time between when the touch event is generated, and when the application receives this event is small, but non-zero. The two timestamps provided by the mobile device represent these two times. The "actionTime" is the timestamp recorded when the touch event is generated (and is provided as part of that touch even object), and teh "callbackTime" is the timestamp recorded immediately when the application's touch handling method is called.



