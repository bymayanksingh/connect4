<div align=center>

<p>
  <img src="./images/logo/c4.gif">
</p>

[![Open Issues](https://img.shields.io/github/issues/code-monk08/connect-four?style=for-the-badge&logo=github)](https://github.com/code-monk08/connect-four/issues)  [![Forks](https://img.shields.io/github/forks/code-monk08/connect-four?style=for-the-badge&logo=github)](https://github.com/code-monk08/connect-four/network/members)  [![Stars](https://img.shields.io/github/stars/code-monk08/connect-four?style=for-the-badge&logo=reverbnation)](https://github.com/code-monk08/connect-four/stargazers)  ![Maintained](https://img.shields.io/maintenance/yes/2019?style=for-the-badge&logo=github)  ![Made with Python](https://img.shields.io/badge/Made%20with-Python-blueviolet?style=for-the-badge&logo=python)  ![Open Source Love](https://img.shields.io/badge/Open%20Source-%E2%99%A5-red?style=for-the-badge&logo=open-source-initiative)  ![Built with Love](https://img.shields.io/badge/Built%20With-%E2%99%A5-critical?style=for-the-badge&logo=ko-fi)  [![Follow Me](https://img.shields.io/twitter/follow/codemonk08_?color=blue&label=Follow%20%40codemonk08_&logo=twitter&style=for-the-badge)](https://twitter.com/intent/follow?screen_name=codemonk08_) 
[![GitHub followers](https://img.shields.io/github/followers/code-monk08.svg?label=Follow&style=for-the-badge&logo=github)](https://github.com/code-monk08/)  [![Slack](https://img.shields.io/badge/Slack-Chat-informational?style=for-the-badge&logo=slack)](https://join.slack.com/t/connectfourgroup/shared_invite/enQtODMxNTAwNDY4NDU0LTZmYTZkMzJiNWQwZDk1YjhlZTEzY2VhMDNkNjVhOGIzNGIyNmYxODM4NWI5MjNjYmJlZjk4MjA4MzQ3MjZhNDg)

</div>

## :ledger: Index

- [About](#beginner-about)
- [Features](#page_facing_up-features)
- [Usage](#zap-usage)
  - [Installation](#electric_plug-installation)
  - [Commands](#package-commands)
- [File Structure](#file_folder-file-structure)
- [Community](#cherry_blossom-community)
  - [Contribution](#fire-contribution)
  - [Branches](#cactus-branches)
- [Guideline](#exclamation-guideline)  
- [Resources](#page_facing_up-resources)
- [Gallery](#camera-gallery)
- [Credit/Acknowledgment](#star2-creditacknowledgment)
- [License](#lock-license)
- [Hall Of Fame](#sparkles-hall-of-fame)

##  :beginner: About
Connect Four is a two-player connection game in which the players first choose a color and then take turns dropping one colored disc from the top into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the lowest available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs.

##  :page_facing_up: Features
 - 2 player interactive game
 - Supports undo operation
 - Supports interactive game sounds
 - Ability to play with computer AI (in development phase)
 - Multiplayer on local network using sockets (in development phase)
 - Ability to customize game theme (in development phase)
 - Cross platform Linux, Windows, Mac (in development phase)

## :zap: Usage
To use this project.

###  :electric_plug: Installation
- Install dependencies & export environment variables.

```bash
$ sudo -H pip3 install -r requirements.txt
```
###  :package: Commands
- Start project using
```bash
$ python3 game.py
```

##  :file_folder: File Structure
- Add a file structure here with the basic details about files, below is current file structure.

```
.
├── assets.py
├── CODE_OF_CONDUCT.md
├── config.py
├── _config.yml
├── connect_game.py
├── events.py
├── game_board.py
├── game_data.py
├── game.py
├── game_renderer.py
├── images
│   ├── blackball91px.png
│   ├── game.svg
│   ├── logo
│   │   ├── c4.gif
│   │   ├── connect4.gif
│   │   └── connect4.png
│   ├── redball90px.png
│   ├── screenshots
│   │   ├── 1.png
│   │   └── 2.gif
│   └── yellowball90px.png
├── LICENSE
├── README.md
├── requirements.txt
├── restart.sh
└── sounds
    ├── disc_drop_1.wav
    ├── disc_drop_2.wav
    └── event.ogg

4 directories, 26 files
```

| No | File Name          | Details
|----|--------------------|-------------------------------------------------------------------------------------|
| 1.  | [assets.py](assets.py)          | used for loading sound and image files in python.
| 2.  | [config.py](config.py)          | contains game's configuration settings.
| 3.  | [connect_game.py](connect_game.py)    | Contains the ConnectGame class which holds the logic for the whole game.
| 4.  | [events.py](events.py)          | Contains classes used to define and hold event data.
| 5.  | [game_board.py](game_board.py)      | Contains the GameBoard data structure and methods which operate on it.
| 6.  | [game_data.py](game_data.py)       | Contains the GameData class, which contains all of the data in the game.
| 7.  | [game_renderer.py](game_renderer.py)   | Holds the GameRenderer class, which renders the game state using sound and graphics.
| 8.  | [game.py](game.py)            | contains connect four game logic.
| 9.  | images/            | contains image resources used in the game.
| 10. | images/logo/        | contains logo used in the README.
| 11. | images/screenshots/ | contains game screenshots.
| 12. | [LICENSE](LICENSE)            | this project uses MIT License.
| 13. | [requirements.txt](requirements.txt)   | contains all the dependencies used in the game.
| 14. | [restart.sh](restart.sh)         | bash script to relaunch the game once it is finished.
| 15. | sounds/            | contains sound resources used in the game.
| 16. | [CODE_OF_CONDUCT.md](https://github.com/code-monk08/connect4/blob/master/CODE_OF_CONDUCT.md) | tells about our responsibilities as a team
- __Dependency Graph__

<p align="center">
  <img src="./images/game.svg" width="800">
</p>

##  :exclamation: Guideline

- __Code Style__

### `black`
In order to maintain the code style consistency across entire project I use a code formatter. I kindly suggest you to do the same whenever you push commits to this project.

The python code formatter I chose is called Black. It is a great tool and it can be installed quickly by running

```bash
sudo -H pip3 install black
```

or

```bash
python3.6 -m pip install black
```

It requires Python 3.6.0+ to run.

- __Usage__

```bash
black {source_file_or_directory}
```

For more details and available options, please check their [psf/black](https://github.com/psf/black).

### `isort`
I also use isort, it is a Python utility / library to sort imports alphabetically, and automatically separated into sections. It provides a command line utility which can be installed using.

```bash
sudo -H pip3 install isort
```

- __Usage__

```bash
isort {source_file}.py
```

For more details and available options, please check their [timothycrosley/isort](https://github.com/timothycrosley/isort).


- __Close Issues__

Close issues using keywords: [how to ?](https://help.github.com/en/articles/closing-issues-using-keywords)

## :cherry_blossom: Community

 ###  :fire: Contribution

 Your contributions are always welcome and appreciated. Following are the things you can do to contribute to this project.

 1. **Report a bug** <br>
 If you think you have encountered a issue, and I should know about it, feel free to report it [here](https://github.com/code-monk08/connect4/issues/new) and I will take care of it.

 3. **Create a pull request** <br>
 It can't get better then this, your pull request will be appreciated by the community. You can get started by picking up any open issues from [here](https://github.com/code-monk08/connect4/issues) and make a pull request.

 > If you are new to open-source, make sure to check read more about it [here](https://www.digitalocean.com/community/tutorial_series/an-introduction-to-open-source) and learn more about creating a pull request [here](https://www.digitalocean.com/community/tutorials/how-to-create-a-pull-request-on-github).

 ### :cactus: Branches

- No other permanent branches should be created in the main repository, you can create feature branches but they should get merged with the master.

##  :page_facing_up: Resources
- [PyGame Documentation](https://www.pygame.org/docs/) : Pygame is a cross-platform set of Python modules designed for writing video games. It includes computer graphics and sound libraries designed to be used with the Python programming language.

##  :camera: Gallery
<p align="center">
  <img src="./images/screenshots/1.png" width="800">
</p>
<p align="center">Start Game Window</p>

<p align="center">
  <img src="./images/screenshots/2.png" width="800">
</p>
<p align="center">Game Play</p>

<p align="center">
  <img src="./images/screenshots/3.gif" width="800">
</p>
<p align="center">Game Play GIF</p>

<p align="center">
  <img src="./images/screenshots/4.png" width="800">
</p>
<p align="center">Restart or Quit as the Game ends.</p>

## :star2: Credit/Acknowledgment
[![Contributors](https://img.shields.io/github/contributors/code-monk08/connect-four?style=for-the-badge)](https://github.com/code-monk08/connect-four/graphs/contributors)

##  :lock: License
[![License](https://img.shields.io/github/license/code-monk08/connect-four?style=for-the-badge)](https://github.com/code-monk08/connect-four/blob/master/LICENSE)

##  :sparkles: Hall Of Fame
[![](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/images/0)](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/links/0)[![](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/images/1)](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/links/1)[![](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/images/2)](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/links/2)[![](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/images/3)](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/links/3)[![](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/images/4)](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/links/4)[![](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/images/5)](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/links/5)[![](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/images/6)](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/links/6)[![](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/images/7)](https://sourcerer.io/fame/code-monk08/code-monk08/connect4/links/7)
