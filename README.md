# Introduction
The BGE supports a form of visual scripting in the form of a Sensor-Controller-Actuator graph which purports to support simple game logic creation. Although a weakly scalable design, the SCA "logic bricks" have become a usable and attractive alternative to learning scripting for BGE users. Whilst it is advisable to learn Python, this dependency must be accounted for in the event of a BGE -> alternative engine transition.

This project aims to produce a simple logic brick export (as JSON) and establish a pure-python implementation for engines such as Panda3D.

## Discrepencies
Because the BGE does not use the same Python API as Panda 3D (the test engine), Python controllers will not natively function when run in the engine. There are some means by which this problem can be addressed:

* Creating an intermediate "compatability API" which both engines define bindings for. Existing must be converted to this API.
* Define a BGE API for Panda, extensively adding support for BGE paradigm features.

It is likely that the second option is the best choice, in the interest of providing utility to the users that are unable to easily port over code (users which would be capable at porting straight to Panda3D API).

This API support should (perhaps) be handled under a separate project,
