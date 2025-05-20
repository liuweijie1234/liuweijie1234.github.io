---
title: Python3 模块 turtle
date: 2022-08-15 10:22:00
tags:
- Python module
- turtle
categories:
- Python
---


![](/images/turtle_01.png)

```python
# -*- coding: utf-8 -*-
import turtle


def main():
    p = turtle.Pen()
    p.pencolor('blue')
    p.pensize('4')
    for x in range(1, 6):
        p.forward(100)
        p.left(216)  # 先向右直⾏，然后左转216°(正五⻆星度数36°)


if __name__ == '__main__':
    main()
```

![](/images/turtle_02.png)

```python
# -*- coding: utf-8 -*-
import turtle
import time

turtle.pensize(5)
turtle.pencolor("yellow")
turtle.fillcolor("red")

turtle.begin_fill()

for _ in range(5):
    turtle.forward(200)
    turtle.right(144)
turtle.end_fill()
time.sleep(2)

turtle.penup()
turtle.goto(-150,-120)
turtle.color("violet")
turtle.write("Done", font=('Arial', 40, 'normal'))
time.sleep(1)

```

![](/images/turtle_03.png)

```python
# -*- coding: utf-8 -*-
import turtle
import time
turtle.color("red", "yellow")
turtle.speed(10)
turtle.begin_fill()

for _ in range(50):
    turtle.forward(200)
    turtle.left(170)
turtle.end_fill()
time.sleep(1)
```