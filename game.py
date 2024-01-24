import pyxel
import random

pyxel.init(200,200)

class Ball():
  def __init__(self):
    self.y = 30
    self.x = 100
    self.direction = True # True: 右方向 False: 左方向
    self.direction2 = True #True: 下方向 False: 上方向

  def move(self,level,pad):

    # x軸方向の動き
    speed = level*2
    if self.direction:
      self.x += speed
    else:
      self.x -= speed
    
    if self.x > 200:
      self.direction = False
    elif self.x < 0:
      self.direction = True

    # y軸方向の動き
    if self.direction2:
      self.y += 4
    else:
      self.y -= 4
      
    if (pad.x < self.x + 10 and self.x - 10 < pad.x + 40) and (180 < self.y + 10 and self.y + 10 <185)and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT): 
      self.direction2 = False
    elif self.y < 0:

      self.direction2 = True

class Pad1():
  def __init__(self):
    self.x = pyxel.mouse_x

  def move(self):
    self.x = pyxel.mouse_x

class Pad2():
  def __init__(self):
    self.x = 100
    self.y = 20

  def move(self):
    if pyxel.frame_count % 30 == 0:
      self.x = random.randint(40,160)
      self.y = random.randint(5,95)


class App():
  def __init__(self):
    self.ball = Ball()
    self.pad1 = Pad1()
    self.pad2 = Pad2()
    self.state = 0 # 0: スタート画面 1: ゲーム中 -1: ゲームーオーバ-
    self.level = 1
    self.success = 0
    self.fail = 0
    pyxel.run(self.update, self.draw)


  def updateScore(self):

    if (self.pad2.y <= self.ball.y and self.ball.y <= self.pad2.y + 5) and (self.pad2.x <= self.ball.x and self.ball.x <= self.pad2.x + 40) and self.ball.direction2 == False:
      self.success += 1
      self.ball.y = 0
      self.ball.x = random.randint(10, 190)

    if self.ball.y > 200:
      self.ball.x = 100
      self.ball.y = 100
      self.fail += 1

  def checkState(self):
    if self.success == 1:
      self.state = 2
    if self.fail == 3:
      self.state = 3

  def update(self):
    if self.state == 0:
      if pyxel.btnp(pyxel.KEY_RETURN):
        self.state = 1
    elif self.state == 1:
      self.ball.move(self.level,self.pad1)
      self.pad1.move()
      self.pad2.move()
      self.updateScore()
      self.checkState() # ゲームオーバーになるかどうか判定

    elif self.state == 2 or self.state == 3:
      if pyxel.btnp(pyxel.KEY_RETURN):
        if self.state == 2:
          self.level += 1
        elif self.state == 3:
          self.level = 1
        # スコアを初期値に戻す
        self.success = 0
        self.fail = 0
        self.state = 1
    
    

  def draw(self):
    pyxel.cls(7)
    pyxel.line(0,100,200,100,1)
    if self.state == 0:
      pyxel.text(60, 70, "GAME START by Press Enter", 0)
    elif self.state == 1:
      # ボール
      if self.ball.direction2:
          color = 4
      else:
          color = 3
      pyxel.circ(self.ball.x, self.ball.y, 10, color)
      # パッド
      padwidth = 40 - self.level * 4
      pyxel.rect(self.pad1.x, 180, padwidth, 5, 3)
      pyxel.rect(self.pad2.x, self.pad2.y, padwidth, 5, 4)
      # スコア
      pyxel.text(10, 10, "Success: " + str(self.success), 0)
      pyxel.text(10, 20, "Fail: " + str(self.fail), 0)
    if self.state == 2:
      pyxel.text(90, 70, "You WIN", 10)
      pyxel.text(40, 80, "Press Enter to next self.level", 0)

    if self.state == 3:
      pyxel.text(90, 70, "YOU LOSE", 5)
      pyxel.text(90, 70, "ONCE AGAIN", 0)

App()
