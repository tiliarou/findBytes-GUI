# findBytes GUI Syntax

When using findBytes GUI, the program expects your offsets in a certain format. Below, you will find details on how to correctly port your offsets!

Note: this tutorial expects you to have already gotten your offsets. If you are not sure how to get offsets, click the "HOW TO" button on the "Type All The Offsets You Wish To Port" screen, when using findBytes GUI.

---

### Let's Begin...

**Porting multiple offsets:**

For each new offset you type, make sure to press `Enter` on your keyboard to create a new line. findBytes GUI expects 	you to have a new offset on each new line.

Ex.

    0035F219
    0117E271
    03820182
etc...


**Porting patches:**

If you are porting IPS-Witch patches, just press enter between each offset & patch. The left side should be the offsets, while the right side should be the patches. 

ex.
		
    003E2618 C0035FD6
    00D36719 1FA28190
		
etc...

---

### Common Mistakes...

1. Don't leave extra lines before, after, or between, offsets/patches!
	
ex.
   00317291

   01038103
   0A171937

2. Remove any spaces before, after, or in the the middle, of your offsets/patches.

ex.
	

    037191389
     018318A12
    0E2618276

3. Either go all offsets, or all patches. Don't do a mixture of both! findBytes GUI will get confused!
ex.
   
    0E271832
    0E271874 C0035FD6
    0E251731 C0035FD6
    0E816221

---

Couldn't find the answer you were looking for? Still have a question?
Hit me up on *Discord*: @AmazingChz#5695
