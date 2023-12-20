# CS2_POC
A Proof-of-Concept cheat developed for CS2 utilizing the PyMem library for handling memory management. 

I was bored and wanted to write a proof-of-concept cheat for CS2 utilizing the PyMem library to handle all my reading/writing memory needs. There are some new caveats 
to working with CS2 when compared to CS:GO, first of all being that the process is now 64-bit which means addresses will now be 8-byte addressable. Additionally structs and methods within the game's memory have altered, and getting information about each entity is a bit more involved now. I chose to utilize python mostly because I've done cheats in C++ in the past and wanted something new. There's also a major lack of open-source Python cheats for CS2.

This is still very barebones and only has about an hour of work put into it, but I plan to explore pattern-scanning, developing an aimbot from scratch, and a few other features before moving onto developing a kernel-driver interface for a new cheat.

Update 12/20/2023:
* Implemented rip-relative addressing for pattern-scanning
* Added simple get player position function
* Extended Pymem to read vec_3d data types from memory


I don't support the malicious usage of this code to gain any unfair advantages and it is solely for educational use.
