Urban Zombie Warrior
Urban Zombie Warrior is a 2D platformer game where you play as Py.Man, navigating through a post-apocalyptic world filled with zombies and obstacles. The goal is to survive as long as possible, defeating zombies by jumping on them and avoiding death.

Table of Contents
Installation
How to Play
Features
Dependencies
Screenshots
License
Installation
1. Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/urban-zombie-warrior.git
cd urban-zombie-warrior/Game
2. Install Dependencies
Make sure you have Python installed (preferably 3.7 or higher). Then, install the required packages:

bash
Copy code
pip install -r requirements.txt
requirements.txt:

Copy code
pygame
numpy
scipy
3. Run the Game
To start the game, navigate to the directory containing main.py and run:

bash
Copy code
python main.py

How to Play
Movement: Use the A key to move left, and the D key to move right.
Jumping: Press the W key to jump.
Objective: Jump on zombies to defeat them, avoid colliding with zombies' sides, and make your way through the platforms.
Menu: Press Enter to start the game from the main menu.
Death: If you die, a "WASTED" message will be displayed. The game will then exit after a few seconds.
Features
Smooth Platforming Mechanics: Navigate through obstacles and platforms with ease.
Enemy Zombies: Jump on zombies to defeat them, or risk dying if they collide with you.
Scrolling Background: Dynamic scrolling as the player moves through the level.
Animated Characters: Both the player and the zombies are animated, with smooth transitions between frames.
Blurred Menu Screen: A Gaussian blur effect is applied to the background when the menu is active.
Dependencies
The game relies on the following Python libraries:

pygame: For handling game mechanics, rendering, and user input.
numpy: For handling the image data in arrays.
scipy: Specifically for applying the Gaussian blur effect on the background during the menu and death screens.
To install these dependencies, use:

bash
Copy code
pip install -r requirements.txt
Screenshots
Main Menu

In-Game

Death Screen

License
This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to modify this README.md to suit your specific needs, such as adding more detailed instructions, additional sections, or screenshots. You can create a folder named screenshots to include images for the "Screenshots" section in the README.