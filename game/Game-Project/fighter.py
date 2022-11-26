import pygame

class Fighter():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
    self.player = player
    self.size_width = data[0]
    self.size_height = data[1]
    self.image_scale = data[2]
    self.offset = data[3]
    self.flip = flip
    self.animation_list = self.load_images(sprite_sheet, animation_steps)
    self.action = 0 #0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
    self.frame_index = 0
    self.image = self.animation_list[self.action][self.frame_index]
    self.update_time = pygame.time.get_ticks()
    self.rect = pygame.Rect((x, y, 80, 180))
    self.vel_y = 0
    self.running = False
    self.jump = False
    self.attacking_1 = False
    self.attacking_2 = False
    self.sp_atk = False
    self.attack_type = 0
    self.attack_cooldown = 0
    self.special_atk_cooldown = 0
    self.attack_sound = sound
    self.hit = False
    self.health = 100
    self.alive = True


  def load_images(self, sprite_sheet, animation_steps):
    #extract images from spritesheet
    animation_list = []
    for y, animation in enumerate(animation_steps):
      temp_img_list = []
      for x in range(animation):
        temp_img = sprite_sheet.subsurface(x * self.size_width, y * self.size_height, self.size_width, self.size_height)
        temp_img_list.append(pygame.transform.scale(temp_img, (self.size_width * self.image_scale, self.size_height * self.image_scale)))
      animation_list.append(temp_img_list)
    return animation_list


  def move(self, screen_width, screen_height, surface, target, round_over):
    SPEED = 7
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0

    #get keypresses
    key = pygame.key.get_pressed()

    #can only perform other actions if not currently attacking
    if self.attacking_1 == False and self.attacking_2 == False and self.sp_atk == False and self.alive == True and round_over == False:
      #check player 1 controls
      if self.player == 1:
        #movement
        if key[pygame.K_a]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_d]:
          dx = SPEED
          self.running = True
        #jump
        if key[pygame.K_w] and self.jump == False:
          self.vel_y = -40
          self.jump = True
        #attack
        if key[pygame.K_r] :
          self.attack_1(target)
          #determine which attack type was used
          if key[pygame.K_r]:
            self.attack_type = 1
          #if key[pygame.K_t]:
            #self.attack_type = 2
        if key[pygame.K_t]:
          self.attack_2(target)
        if key[pygame.K_y] and self.health < 40 : #can only perform special attack if the player health is < then 50
          self.special_atk(target)



    if self.attacking_1 == False and self.attacking_2 == False and self.sp_atk == False and self.alive == True and round_over == False:
      #check player 2 controls
      if self.player == 2:
        #movement
        if key[pygame.K_LEFT]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_RIGHT]:
          dx = SPEED
          self.running = True
        #jump
        if key[pygame.K_UP] and self.jump == False:
          self.vel_y = -40
          self.jump = True
        #attack
        if key[pygame.K_KP1] :
          self.attack_1(target)
          #determine which attack type was used
          if key[pygame.K_KP1]:
            self.attack_type = 1
          
        if key[pygame.K_KP2] :
          self.attack_2(target)
        if key[pygame.K_KP3] and self.health < 40 :
          self.special_atk(target)


    #apply gravity
    self.vel_y += GRAVITY
    dy += self.vel_y

    #ensure player stays on screen
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 110 - self.rect.bottom

    #ensure players face each other
    if target.rect.centerx > self.rect.centerx:
      self.flip = False
    else:
      self.flip = True

    #apply attack cooldown
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1
    if self.special_atk_cooldown > 0 :
      self.special_atk_cooldown -= 1

    #update player position
    self.rect.x += dx
    self.rect.y += dy


  #handle animation updates
  def update_p1(self):
    #check what action the player is performing
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(12)#6:death
    elif self.hit == True :
      self.update_action(11)#5:hit
    elif self.attacking_1 == True:
      if self.attack_type == 1:
        self.update_action(6)#3:attack1
      #elif self.attack_type == 2:
        #self.update_action(8)#4:attack2
    elif self.jump == True:
      self.update_action(3)#2:jump
    elif self.running == True:
      self.update_action(1)#1:run
    elif self.attacking_2 == True :
      self.update_action(4) #attack 3
    elif self.sp_atk == True :
      self.update_action(9)
    else:
      self.update_action(0)#0:idle
    
    animation_cooldown = 80
    #update image
    self.image = self.animation_list[self.action][self.frame_index]
    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #check if the animation has finished
    if self.frame_index >= len(self.animation_list[self.action]):
      #if the player is dead then end the animation
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
        #check if an attack was executed
        if self.action == 6 or self.action == 8:
          self.attacking_1 = False
          self.attack_cooldown = 20
        if self.action == 4 :
          self.attacking_2 = False
          self.attack_cooldown = 40
        if self.action == 9 :
          self.sp_atk = False
          self.special_atk_cooldown = 5000
        #check if damage was taken
        if self.action == 11:
          self.hit = False
          #if the player was in the middle of an attack, then the attack is stopped
          self.attacking_1 = False
          self.attack_cooldown = 20
          self.attacking_2 = False
          self.attack_cooldown = 20
          self.sp_atk = False
          


  


  def update_p2(self):
  #check what action the player is performing
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(14)#6:death
    elif self.hit == True:
      self.update_action(13)#5:hit
    elif self.attacking_1 == True:
      if self.attack_type == 1:
        self.update_action(7)#3:attack1
      #elif self.attack_type == 2:
       # self.update_action(8)#4:attack2
    elif self.jump == True:
      self.update_action(3)#2:jump
    elif self.running == True:
      self.update_action(1)#1:run
    elif self.attacking_2 == True :
      self.update_action(5) #attack2
    elif self.sp_atk == True :
      self.update_action(10)
    else:
      self.update_action(0)#0:idle





    animation_cooldown = 80
    #update image
    self.image = self.animation_list[self.action][self.frame_index]
    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #check if the animation has finished
    if self.frame_index >= len(self.animation_list[self.action]):
      #if the player is dead then end the animation
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
        #check if an attack was executed
        if self.action == 7 or self.action == 8:
          self.attacking_1 = False
          self.attack_cooldown = 20
        if self.action == 5 :
          self.attacking_2 = False
          self.attack_cooldown = 40
        if self.action == 10 :
          self.sp_atk = False
          self.special_atk_cooldown = 5000
        #check if damage was taken
        if self.action == 13:
          self.hit = False
          #if the player was in the middle of an attack, then the attack is stopped
          self.attacking_1 = False
          self.attack_cooldown = 20
          self.attacking_2 = False
          self.attack_cooldown = 20
          self.sp_atk = False   
          



  def attack_1(self, target):
    if self.attack_cooldown == 0:
      #execute attack
      self.attacking_1 = True
      self.attack_sound.play()
      attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):
        target.health -= 10
        target.hit = True
  

  def attack_2(self, target):
    if self.attack_cooldown == 0:
      #execute attack
      self.attacking_2 = True
      self.attack_sound.play()
      attacking_rect = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip), self.rect.y, 3 * self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):
        target.health -= 20
        target.hit = True

  
  def special_atk(self, target):

      if self.special_atk_cooldown == 0:
        #execute special attack
        self.sp_atk = True
        self.attack_sound.play()

        attacking_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip), self.rect.y, 4 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect) :
          target.health -= 50
          target.hit = True
  
 



  def update_action(self, new_action):
    #check if the new action is different to the previous one
    if new_action != self.action:
      self.action = new_action
      #update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))