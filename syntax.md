# findBytes GUI's Syntax

When using findBytes GUI, the program expects your offsets in a certain format. Below, you will find details on how to correctly port your offsets!

***Note:*** this tutorial expects you to have already gotten your offsets. If you are not sure how to get offsets, click the `HOW TO` button on the `Type All The Offsets You Wish To Port` screen, when using findBytes GUI.

---

## Let's Begin...

**Porting multiple offsets:**

For each new offset you type, make sure to press `Enter` on your keyboard to create a new line. findBytes GUI expects you to have a new offset on each new line.

example:

    0035F219
    0117E271
    03820182

---

**Porting patches:**

If you are porting IPS-Witch patches, just press enter between each offset & patch. The left side should be the offsets, while the right side should be the patches. Do not include the comment or `@enabled` in IPS-Witch patches, into findBytes GUI. Just type in the actual patches.

example:
		
    003E2618 C0035FD6
    00D36719 1FA28190

---

## Common Mistakes...

1. Don't leave extra lines before, after, or between offsets/patches!
	
example:

    00317291

    01038103
    0A171937
    
---

2. Remove any spaces before, after, or in the the middle of your offsets/patches.

example:
	

    037191389
     018318A12
    0E2618276
    
---

3. Either go all offsets, or all patches. Don't do a mixture of both! findBytes GUI will get confused!

example:
   
    0E271832
    0E271874 C0035FD6
    0E251731 C0035FD6
    0E816221

---

4. Don't include name-comments or `@enabled` (found in IPS-Witch patches) when typing in your patch into findBytes GUI.

example:

    // Offline Shop [Zewia] (4.3.0)
    @enabled
    0138F628 200080D2
    
---

Couldn't find the answer you were looking for? Still have a question?
Hit me up on *Discord*: **@AmazingChz#5695**
