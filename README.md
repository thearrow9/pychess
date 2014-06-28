# PyChess
pychess е реализация на игра на шахмат срещу компютър.

## Изисквания

python 3.4

## Реализирани функционалности

* зареждане на произволна позиция чрез [FEN нотация](http://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation) и валидирането й
* изиграване само на легални ходове
* специални ходове (рокада, ан-пасан, произвеждане)
* проверки дали позицията е реми (пат, трикратно повторение, [правилото за 50 хода](http://en.wikipedia.org/wiki/Fifty-move_rule))
* елементарни критерии за оценка на позицията
* Интегриране на third party анализатор (в момента се поддържа само [Stockfish](https://github.com/mcostalba/Stockfish))

## Добавяне на изкуствен интелект (по желание)

Ако искате да играете срещу компютър, първо ще трябва да го инсталирате:

```
sudo apt-get install git g++
cd engines/
git clone https://github.com/mcostalba/Stockfish.git
cd Stockfish/src
make profile-build ARCH=x86-64 # или ARCH=x86-32
```

## Демо

```
$ python3.4 play.py [-c, --color=<color>] [-p, --position=<fen>] [-s, --strength=<strength>]
```

, където:

* &lt;color&gt; е цвета фигури, с които играе компютъра (пропуснете ако не желаете опонент) 0-2 цвята in ('white', 'black')
* &lt;fen&gt; е произволна позиция
* &lt;strength&gt; е число от 1 до 20 (20 е непобедим)

Ходовете се играят по следния начин:

```
from-to
```

, където:

* from е полето, на което се намира фигурата
* to е полето, където отива.

Примери: e2-e4, e4-d5, e1-g1 (рокада)
