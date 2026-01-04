# 2D Videogame called True Name

## Description

Simple videogame where player tries to guess word from table, using nothing more than a brush and pattern matching. It is part of my semestral work for subjects **Bi-Pyt** and **Bi-Mvt**.

![Idle menu](/assets/readme/out.gif)

## Dependencies

* [Pygames](https://www.pygame.org/wiki/GettingStarted) <pre><code>python3 -m pip install -U pygame --user</code></pre>

* [Pillow](https://pillow.readthedocs.io/en/stable/) <pre><code>python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow</code></pre>

* [Pytorch, torchvision](https://pytorch.org/) <pre><code>python3 -m pip install torch torchvision </code></pre>

* [timm](https://pypi.org/project/timm/)<pre><code>pip install timm</code></pre>

* [Pytest](https://docs.pytest.org/en/stable/#)<pre><code>pip install -U pytest</code></pre>

## How to start

1. Clone into my repository, create python [virtual enviroment](https://www.w3schools.com/python/python_virtualenv.asp) and install all the necessary dependencies listed [above](#dependencies) to your newly created virtual enviroment.

2. To start the game you simply activate your virtual enviroment, enter games root folder and enter command to your console <pre><code>python3 main.py</code></pre>

## How to play

### Start menu

* Clicking on NEW GAME button your **health** and **coins** will be reseted. When playing for the first time you will have no other choice. 

* Clicking on Continue button you will continue with same **health** and **coins** as when you stopped playing.

    ![new_game](/assets/readme/star_menu.png)

### Main menu

![main_menu](/assets/readme/main_menu.png)

* By clicking on one of 3 **contracts** on bounty wall you will inspect a **contract**. You can **accept** contract by clicking on **check mark** and enter a **level**. By clicking on **x mark** you will return back to menu.

    ![contract](/assets/readme/contract.png)

* By clicking on **wizzard** you enter shop where you can upgrade your **health** in exchange for a few **coins**. By clicking on **wizzard** again you return back to menu.

    ![shop](/assets/readme/shop.png)

### Level

To **exit** level and earn **reward** you need to guess one specific word from the table. Each level consists of 3 parts plus 1 exit gate. To move between areas use **movement vines** on sides of your screen.
![level - movement](/assets/slider/slider.png)

* **Table** area is where you will look for **english word**, **name** or **activity**.

    ![level - table](/assets/readme/level_table.png)

* **Canvas** area is place where you **spell** chosen word by you. You do that by **drawing** each letter separetly into frames. **Drawing** is done by holding **left mouse button** and **moving** your mouse. When you are done press **spacebar** to confirm your guess. When system recognizes your letter wrongly, you can **redo** it by pressing **right mouse button** **inside** frame with wrongly recognized letter. Be careful each stroke costs you **health**. After running out of **health** you **exit** level with no **reward**.

    ![level - canvas](/assets/readme/level_canvas.png)

* **Evaluation** area is place where your answers will be evaluated. Each word has **likness** atribute. **Likness** means on how many possitions has word matching letters with the word you are looking for.*(Let's imagine you are looking for word: table, and you guess word: turn. Word turn has likness = 1 because it is matching with the word you are looking for on 1 position. That position is the first postion. For example word cable would have likness = 3 because it is matching with the word you are looking for on different 3 positons.)*

    ![level - guess](/assets/readme/level_guess.png)

* After guessing right word, the word will stay written inside frames in **canvas** area. Also new **movement vines** will appear in **canvas** area. By clicking on them you will move to **exit** area. After clicking on the **door** you will **exit** level and gain promised **reward**.

    ![level - exit](/assets/readme/level_exit.png)

## How to run tests

* To run all tests you need to go to games root folder and enter command<pre><code>python3 -m pytest</code></pre>
* To run tools tests you need to go to games root folder and enter command<pre><code>python3 -m pytest tests/test_tools</code></pre>
* To run scene tests you need to go to games root folder and enter command<pre><code>python3 -m pytest tests/test_scenes</code></pre>