import pygame
import random
from pygame.color import Color
from pygame.sprite import Sprite
from pygame.surface import Surface
from runner import Runner

FPS = 28

x = 50
y = 50
width = 40
height = 60
vel = 5

isJump = False
jumpCount = 10


class Bullet(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((20, 20))
        pygame.draw.rect(self.image,
                         Color(255, 0, 0),
                         (0, 0, 20, 20))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= 15 # 미사일 속도

if __name__ == "__main__":
    pygame.init()

    size = (400, 300)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Runner Anomation")

    run = True
    clock = pygame.time.Clock()

    background_img = pygame.image.load("background.png")

    runner1 = Runner()
    runner1.rect.x = 0
    runner1.rect.y =170

    runner2 = Runner()
    runner2.rect.x =130
    runner2.rect.y = 170

    runner3 = Runner()
    runner3.rect.x = 250
    runner3.rect.y = 170

    runner_group = pygame.sprite.Group()
    runner_group.add(runner1)
    runner_group.add(runner2)
    runner_group.add(runner3)

    bullet = Bullet()
    bullet.rect.x = screen.get_width()
    bullet.rect.y = random.randint(200,260) # 200부터 260사이의 정수중 미사일 높이
    bullet_group = pygame.sprite.Group()
    bullet_group.add(bullet)

    #게임 루프
    while run:
        
        # 1) 사용자 입력 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and runner1.rect.x > vel:
            runner1.rect.x -= 5
            
        if keys[pygame.K_RIGHT] and runner1.rect.x < 500 - vel - width:
            runner1.rect.x += 5
            
        if not(isJump):
            if keys[pygame.K_UP] and runner1.rect.y > vel:
                runner1.rect.y -= 5

            if keys[pygame.K_DOWN] and runner1.rect.y < 500 - height - vel:
                runner1.rect.y += 5

            if keys[pygame.K_SPACE]:
                isJump = True
        else:
            print(isJump, jumpCount)
            if jumpCount >= -10:
                runner1.rect.y -= (jumpCount * abs(jumpCount)) * 0.5
                jumpCount -= 1
            else:
                jumpCount = 10
                isJump = False
            

        # 2) 게임 상태 업데이트
        runner_group.update()
        bullet_group.update()
        collided = pygame.sprite.groupcollide(
            bullet_group, runner_group, False, True)
        if len(collided.items()) > 0:
            print("남은 Runner 수 : {0}".format(len(runner_group.sprites())))

        # 3) 게임 상태 그리기
        screen.blit(background_img, screen.get_rect())
        runner_group.draw(screen)
        bullet_group.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)


pygame.quit()
