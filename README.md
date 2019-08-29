# findBytes GUI
*Port your patches, update your offsets - Nintendo Switch*

---

[findBytes](https://gist.github.com/3096/ffd6d257f148aab0b74bfc50dfe43e80) is a tool originally developed by [Dualie](https://github.com/3096), which helps find offsets in different versions of Nintendo Switch games. I then decided to make a nice UI out of it, because who doesn't like UIs?

---

# *Features:*
 - Port full [IPS-Witch](https://github.com/3096/ipswitch/releases) patches.
 - Port multiple offsets at a time.
 - Continuously port offsets from *same* or *different* files.
 - Decompress your ***.NSO** file(s) via "**decompressNSO.bat**".
 - Clean, easy to understand UI.
 

---
---
---

## How to Run Source Code:

  - Download and install [Python 3.6.3](https://www.python.org/downloads/release/python-363/) (make sure to check "**Add Python 3.6 to PATH**" in the installer. Otherwise, "**pip3**" won't work!)

  - Install PyQt5 and PyGithub (run "**pip3 install PyQt5 PyGithub**" in *Terminal*, after downloading [Python 3.6.3](https://www.python.org/downloads/release/python-363/))
  
  - Download and extract [findBytes](https://gist.github.com/3096/ffd6d257f148aab0b74bfc50dfe43e80)
  
  - Put [findBytes.py](https://gist.github.com/3096/ffd6d257f148aab0b74bfc50dfe43e80) into `/resources/tools/findBytes/`
  
  - Run "**main.py**", and follow its instructions
  
---

## Credits:

  - **Dualie:** Programmed the actual offset porter ([findBytes](https://gist.github.com/3096/ffd6d257f148aab0b74bfc50dfe43e80))

  - **AmazingChz:** Programmed the GUI (**findBytes GUI** [[this!](https://github.com/AmazingChz/findBytes-GUI/releases/latest)])

  - **SciresM:** Programmed [hactool](https://github.com/SciresM/hactool/releases/latest) (what we use to decompress our ***.NSO** files)
  
---

# *For support, join our Discord server:* <a href="https://discord.gg/mmhgFQk"><img src="https://discordapp.com/api/guilds/427932365457719297/widget.png?style=shield" /></a>
