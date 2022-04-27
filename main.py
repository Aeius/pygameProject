# pygame 필수 import
import pygame, sys, random, time
from pygame.locals import *
# 파일 경로를 생성 및 수정하고 파일 정보를 쉽게 다룰 수 있게 해주는 모듈

# pygame초기화
pygame.init()
# 시계 설정
FramePerSec = pygame.time.Clock()

# 화면 크기 지정 상수
HEIGHT = 650
WIDTH = 400

# 화면 설정
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))

# 게임 타이틀 설정
pygame.display.set_caption("Game")

# 색 지정
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# 출력할 글자의 폰트 설정
font = pygame.font.SysFont("Verdana", 60)  # 큰 폰트 설정
font_small = pygame.font.SysFont("Verdana", 30)  # 작은 폰트 설정
font_smaller = pygame.font.SysFont("Verdana", 15)  # 작은 폰트 설정
game_title = font.render("Jump Up", True, BLACK)  # 게임시작 화면 문구 설정
level_inpo = font_small.render("Level Seclet", True, BLACK)  # 게임시작 화면 문구 설정
level_1 = font_small.render("1", True, BLACK)  # 게임시작 화면 문구 설정
level_2 = font_small.render("2", True, BLACK)  # 게임시작 화면 문구 설정
level_3 = font_small.render("3", True, BLACK)  # 게임시작 화면 문구 설정
level_1s = font_small.render("1", True, RED)  # 게임시작 화면 문구 설정
level_2s = font_small.render("2", True, RED)  # 게임시작 화면 문구 설정
level_3s = font_small.render("3", True, RED)  # 게임시작 화면 문구 설정
title_inpo = font_small.render("Press SpaceBar to start", True, BLACK)  # 게임시작 화면 문구 설정
game_over = font.render("Game Over", True, BLACK)
restart = font_smaller.render("Press SpaceBar to start or Press X to Quit", True, BLACK)  # 게임시작 화면 문구 설정

# 출력할 소리들 설정
sound_jump = pygame.mixer.Sound("static/sound_jump.ogg")
sound_coin = pygame.mixer.Sound("static/sound_coin.ogg")
sound_bgm = pygame.mixer.music
sound_bgm.load("static/sound_bgm.ogg") # bgm설정
sound_gameover = pygame.mixer.Sound("static/sound_gameover.wav")

# 출력할 소리 크기 설정
sound_bgm.set_volume(0.1)
sound_coin.set_volume(0.1)
sound_jump.set_volume(0.1)
sound_gameover.set_volume(0.1)

# bgm 시작
sound_bgm.play(-1)

# 벡터 사용을 위한 함수 호출하여 변수 선언
vec = pygame.math.Vector2  # 2 for two dimensional

# ACC상수 와 FRIC 라는 변수 를 보셨을 것 vec입니다.
# 이것들은 뒷부분에서 사실적인 움직임을 만들고 중력을 구현하는 데 사용할 것입니다.
ACC = 0.5  # 가속도 올릴수록 빨라짐
FRIC = -0.12  # 음수 값이 커질 수록 느려짐 = 마찰이 심해짐 0에 가까워질수록 잘 미끄러짐
FPS = 60

# 게임난이도 설정
FLAT_WIDTH = 0
FLAT_MIN = 6
FLAT_MAX = 7
FLAT_GEN = 8


# 플레이어 클래스 생성
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 플레이어 캐릭터 모양 생성
        # self.surf = pygame.Surface((30, 30))
        # 플레이어 이미지 로드
        self.surf = pygame.image.load("static/player.png")
        self.surf = pygame.transform.scale(self.surf, (30, 30))

        # 플레이어 캐릭터의 색상 지정
        # self.surf.fill((255, 255, 0))
        # 플레이어 캐릭터의 시작 위치 지정
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))

        # 첫 번째 매개변수는 가속도/속도를 나타내고
        # 두 번째 매개변수 X axis는 Y axis. center 매개변수를 제거했습니다.
        # 이는 플레이어의 위치 제어를 self.pos변수로 이동했기 때문입니다.
        # 다음은 move()플레이어를 제어할 수 있는 기능입니다.
        self.pos = vec((WIDTH / 2, HEIGHT - 60))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        # 플레이어가 점프 위치에 있는지 여부를 결정
        self.jumping = False
        # 스코어 점수 최초 값 생성 및 초기화
        self.score = 0

    def move(self):
        # 첫번째 파라미터는 수평 가속도를 나타내고 두번재 파라미터는 수직 가속도를 나타낸다.
        # 여기서 우리가 하고 있는 것은 플레이어에게 0.5의 영구적인 수직 가속도를 제공하는 것입니다.
        # 다시 말해서, 우리는 일정한 중력을 만들었습니다. 0.5의 값은 변경이 가능하다.
        self.acc = vec(0, 0.5)

        # 가속도 0으로 설정
        # self.acc = vec(0, 0)

        # 키눌림 확인
        pressed_keys = pygame.key.get_pressed()

        # 왼쪽이 눌려졌을 경우 가속도가 음수으로 설정됨
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC

        # 오른쪽이 눌려졌을 경우 가속도가 양수로 설정됨
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        # 가속도 설정 변수의 값 FRIC을 조정하여 미끄러짐 마찰의 정도를 조정할 수 있다.
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # 화면 양끝으로 갈 경우 반대쪽으로 나오게하는 코드
        # 물론 이 기능을 원하지 않는 경우 두 개의 if 문을 다른 용도로 사용하고 전체 코드를 둘러싸서 화면에서 벗어나지 않도록 할 수 있습니다.
        # 아래 코드가 아예 없을 경우 객체가 그냥 화면 밖으로 나가버림
        # 못나가게 막으려면 if문 하나에 두개 똑같이 WIDTH WIDTH 넣거나 0 0 넣으면 됨
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        # 이동 후 새 위치로 Player 객체 업데이트 하는 코드
        self.rect.midbottom = self.pos

    # 점프 하는 메서드 위로 올라가기때문에 플레이어 객체에 수직속도 값을 음수 값을 줘야함
    # 그리고 버튼을 눌렀을 때 해당 메서드를 호출
    def jump(self):
        # 점프소리출력
        sound_jump.play()
        # 무한 점프 방지 코드 바닥과 붙어 있는지 확인
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15


    # 점프 메커니즘을 수정하기 위한 메서드 정의
    # 소점프 기능(스페이스바를 떼면은 실행되는 메서드 플레이어의 속도를 줄이는 목적의 메서드)
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    # 플랫폼에 착지 할 수 있도록 하는 메서드
    def update(self):
        # P1(플레이어)와, platforms 그룹에 포함된 스프라이트가 부딪혔을때 충돌 여부 return (마지막 파라매터는 삭제여부 이기때문에 False)
        hits = pygame.sprite.spritecollide(self, platforms, False)
        # 무한 점프 방지 코드 가속도가 1이라도 있으면 안되게
        if self.vel.y > 0:
            if hits:
                # 플레이어의 y 포지션이 플랫폼 바닥위로 올라가지않을 때까지 착륙이 등록되지 않도록함
                if self.pos.y < hits[0].rect.bottom:
                    # 스코어 증가 코드
                    # 방금 착지한 플랫폼의 포인트 속성을 확인한다.
                    # 플랫폼이 생성될 때 기본 point값이 True로 설정되어있으므로 속성을 확인하여 True일 경우
                    # 점수를 상승 시키고 point의 값을 False로 바꿔주는 것
                    # 이렇게 하면 플레이어가 같은 플랫폼으로 계속해서 점프하여 점수를 얻는 것을 방지할 수 있습니다.
                    if hits[0].point == True:  ##
                        hits[0].point = False  ##
                        self.score += 100
                    # 첫번째 코드를 사용하여 Player의 속도를 0으로 설정해야 합니다 self.vel.y = 0. 수직 속도만 0으로 설정했습니다.
                    # 그렇지 않으면 플랫폼에서 수평으로 이동할 수 없습니다
                    # 두번째, 플랫폼의 상단 y 좌표 self.pos.y 로 변수를 업데이트하여 플랫폼 상단에 플레이어를 재배치합니다 .
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    # 수직방향 가속도가 있는 상태면 점프 불가능
                    self.jumping = False


class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # # 플랫폼의 모양 생성
        # self.surf = pygame.Surface((WIDTH, 20))
        # # 플랫폼의 색상 지정
        # self.surf.fill((255, 0, 0))
        # # 플랫폼의 시작 위치 지정
        # self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))

        # 가로 길이가 50 ~ 100 픽셀의 플랫폼을 랜덤 생성
        self.surf = pygame.Surface((random.randint(50, 100) - FLAT_WIDTH, 12))
        # 플랫폼의 색상 지정
        self.surf.fill((0, 255, 0))
        # 플랫폼의 생성 위치 지정
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))
        # 플랫폼 움직임 무작위 방향(왼쪽,오른쪽,가만히) 설정 및 활성화
        self.speed = random.randint(-1, 1)
        self.moving = True
        # 플랫폼에 대한 "포인트" 속성을 생성하여 플레이어가 플레이어에게 착지할 경우
        # 플랫폼에서 포인트를 줄 것인지 여부를 결정합니다. 참이면 예, 거짓이면 아니요.
        self.point = True

    # 플랫폼 움직임 메서드 정의
    def move(self):
        # 플레이어와 플랫폼의 충돌확인
        hits = self.rect.colliderect(P1.rect)
        # 플랫폼이 움직임이 활성화되어있을때 (Base 플랫폼때문에 활성화여부 구분)
        if self.moving == True:
            # self.speed의 방향대로 이동하는데
            self.rect.move_ip(self.speed, 0)
            # 충돌이 있을 경우 플레이어의 속도도 플랫폼이 움직이고 있는 속도와 같아지도록 설정
            if hits:
                P1.pos += (self.speed, 0)
            # 각각의 플랫폼이 화면끝으로 갈 경우 반대편으로 나오도록하는 것
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    # 코인 생성 메서드 정의
    # 멈춰있는 플랫폼 위에 코인을 생성하고 이를 코인 그룹에 추가하는 역할을 합니다.
    def generateCoin(self):
        if (self.speed == 0):
            coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))


# 코인 클래스 정의
class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # 코인 이미지 불러오기
        self.image = pygame.image.load("static/coin.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        # 코인에 사각형 판정 만들기
        self.rect = self.image.get_rect()

        self.rect.topleft = pos

    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 1
            sound_coin.play()  # 코인 먹는 사운드 출력
            self.kill()


# 플랫폼들이 서로 모여 있지 않도록 하는 check() 메서드 정의
# 이 함수는 새로 생성된 플랫폼을 입력으로 사용하고
# 모든 플랫폼이 저장되는 "groupies"라는 Sprite 그룹을 사용합니다.
# 현재 이 새로 생성된 플랫폼은 Sprite 그룹에 그려지거나 추가되지 않았습니다.
# 이 검사를 통과한 경우에만 추가됩니다.
def check(platform, groupies):
    # 충돌 판정 확인 충돌나면 True 리턴
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    # 충돌은 아니지만 근처에 있을 경우 파악
    else:
        for entity in groupies:
            # 새로 생성될 groupies에서 나온 entity 객체들 중
            # 각각의 플랫폼의 간격을 50px 을 보장하기 위한 코드
            if entity == platform:
                continue
            # 절대값을 이용하여 이미 생성되있는 플랫폼(platform)의 위쪽좌표와 생성될 플랫폼(entity)의 아래쪽 좌표의 차이 그리고
            # 생성된 플랫폼(platform)의 아래쪽 좌표와 생성될 플랫폼(entity)의 위쪽 좌표 차이를 50으로 설정
            if (abs(platform.rect.top - entity.rect.bottom) < 55) and (
                    abs(platform.rect.bottom - entity.rect.top) < 55):
                return True
        C = False


def plat_gen():
    # 플랫폼 리젠 함수 정의
    # 이 값은 초기 플랫폼 생성(5 – 6)에 대해 제공한 값보다 커야 합니다.
    # 이 값이 초기 플랫폼 수보다 크지 않으면 플레이어가 HEIGHT / 3화면에 도달할 때까지 새 플랫폼이 생성되지 않습니다.
    # 그 결과 플레이어와 다음 플랫폼 사이에는 한 번의 점프로 커버할 수 없는 큰 간격이 생깁니다.
    while len(platforms) < FLAT_GEN:
        # 새 플랫폼을 만드는 데 임의의 너비 할당 플랫폼의 다양성을 위해
        width = random.randrange(50, 100)
        p = None
        C = True

        # C 가 False를 반환하면 루프가 종료 되고 플랫폼이 그룹에 추가됨
        while C:
            p = platform()
            # 화면의 보이는 부분 바로 위에 플랫폼을 만들고 배치합니다. 위치는 무작위 라이브러리 를 사용하여 무작위로 생성됩니다 .
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            C = check(p, platforms)

            # 생성된 플랫폼 스프라이트 그룹에 추가
        p.generateCoin()  # <----------------
        platforms.add(p)
        all_sprites.add(p)


# 정의한 클래스의 객체 생성
PT1 = platform()
P1 = Player()

# platform()함수를 재정의하여서 바닥플랫폼이 없기때문에 따로 정의해준 것
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255, 0, 0))
PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 50))

# 생성한 모든 객체들을 스프라이트 그룹에 포함
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

# platforms 스프라이트 그룹 생성 및 플랫폼 객체들 해당 그룹에 추가
platforms = pygame.sprite.Group()
platforms.add(PT1)

# coins 스프라이트 그룹 생성
coins = pygame.sprite.Group()

# Base 플랫폼 움직임 비활성화
PT1.moving = False
# Base 플랫폼에서 포인트 기능을 비활성화합니다.
PT1.point = False

# 게임 초기 레벨 생성
for x in range(random.randint(FLAT_MIN, FLAT_MAX)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    # 생성된 플랫폼 스프라이트 그룹에 추가
    pl.generateCoin()  # <----------------
    platforms.add(pl)
    all_sprites.add(pl)


# 메인화면 출력을 위한 게임 시작 변수 및 레벨 조정 변수 시간 변수 설정
game_start = False
LEVEL = 1
now_level = "Easy"
start_time = int(time.time())
remain_time = 0
HS_FILE = "static/highscore.txt" # 하이스코어가 저장될 텍스트 파일

# 하이스코어 파일을 로드하여 해당 파일의 값을 불러오는 메서드
f = open(HS_FILE, 'r')
# 파일안에 적혀져 있는 한줄 = 하이스코어 를 변수에 저장
highscore = f.readline()
# 파일을 열었으면 닫아주는 것도 중요하다
f.close()

print(highscore)
while True:
    # 메인 화면
    displaysurface.fill(GRAY)
    displaysurface.blit(game_title, (20, 150))
    displaysurface.blit(level_inpo, (20, 250))
    displaysurface.blit(title_inpo, (20, 350))
    if LEVEL == 1:
        displaysurface.blit(level_1s, (20, 300))
        displaysurface.blit(level_2, (40, 300))
        displaysurface.blit(level_3, (60, 300))
        FLAT_WIDTH = -15
    elif LEVEL == 2:
        displaysurface.blit(level_1, (20, 300))
        displaysurface.blit(level_2s, (40, 300))
        displaysurface.blit(level_3, (60, 300))
        FLAT_WIDTH = 15
    else:
        displaysurface.blit(level_1, (20, 300))
        displaysurface.blit(level_2, (40, 300))
        displaysurface.blit(level_3s, (60, 300))
        FLAT_WIDTH = 35

    # 모든 이벤트 처리 코드
    for event in pygame.event.get():
        # 윈도우창 종료 버튼 클릭 시 정상종료 되도록하는 코드
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # 스페이스바 눌렸을 때 확인해서 jump()함수 호출
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        # 스페이스바 키를 뗐을 때 확인해서 cancel_jump() 함수 호출
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

        # 메인 화면에서만 작동할 이벤트들
        if game_start == False:
            # 스페이스바 입력 시 게임 시작
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_start = True
            # 오른쪽 왼쪽 키를 이용하여 레벨 지정
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if LEVEL == 1:
                        pass
                    elif LEVEL == 2:
                        LEVEL = 1
                        now_level = "Easy"
                    else:
                        LEVEL = 2
                        now_level = "Normal"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if LEVEL == 1:
                        LEVEL = 2
                        now_level = "Normal"
                    elif LEVEL == 2:
                        LEVEL = 3
                        now_level = "Hard"
                    else:
                        pass

    if game_start == True:
        # 게임 시작 함수
        P1.update()

        # 화면 무한 스크롤
        # 화면에 대한 플레이어의 위치 확인
        # 언제 화면을 이동 시킬지에 대해서 결정하는 지점
        # 화면크기, 플레이어 속도 등을 고려하여 적절한 위치로 선정해야함
        # 플레이어가 해당 위치에 도달할 때마다 안의 코드가 실행됨
        if P1.rect.top <= HEIGHT / 3:
            # 화면은 더이상 동적개체가 아니므로 화면이 이동함에 따라 플레이어의 위치도 업데이트 해줘야함
            # abs()함수를 사용하여 속도 값에서 음수 부호 제거 (abs()함수는 파라미터로 받은 수의 절대값을 반환하는 함수)
            P1.pos.y += abs(P1.vel.y)
            # 다른 플랫폼들도 위치를 업데이트 하기 위해서 abs()함수 이용하여 음수 부호 제거
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                # 플랫폼의 위치가 바닥에서 화면을 벗어나는 모든 플랫폼들을 파괴하는 코드
                # 이 줄이 없으면 플랫폼들이 계속 메모리에 쌓여 게임속도가 느려짐!
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    P1.score += 10  # 바닥이 없어지면 50점 추가
            # 마찬가지로 코인들도 위치를 업데이트 하기 위해서 abs() 함수 이용하여 음수 부호 제거
            for coin in coins:
                coin.rect.y += abs(P1.vel.y)
                if coin.rect.top >= HEIGHT:
                    coin.kill()

        # 플랫폼 리젠 함수 호출
        plat_gen()
        # 배경색 지정
        displaysurface.fill(BLACK)
        # 난이도 및 스코어 표시(앞줄은 폰트 지정)
        font_l = pygame.font.SysFont("Verdana", 20)
        score = font_l.render(str(P1.score), True, (123,255, 0))
        level = font_l.render(now_level, True, (123, 255, 0))
        displaysurface.blit(level, (10, 10))
        displaysurface.blit(score, (WIDTH / 2, 10))

        # 제한 시간을 설정 및 게임 화면에 표시하기
        remain_time = 60 - (int(time.time()) - start_time)
        remain_time_image = font_l.render('Time {}'.format(remain_time), True, (123, 255, 0))
        displaysurface.blit(remain_time_image, (WIDTH - 10 - remain_time_image.get_width(), 10))

        # 코인 생성
        for coin in coins:
            displaysurface.blit(coin.image, coin.rect)
            coin.update()

        # 모든 스프라이트 블러오기
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        # 게임 오버 화면 구현
        if P1.rect.top > HEIGHT or remain_time == -1:
            # 모든 스프라이트 제거
            for entity in all_sprites:
                entity.kill()
                # 0.5초간 정지 후
                time.sleep(0.5)
                sound_bgm.stop()  # bgm 끄기
                sound_gameover.play()  # Game over 사운드 출력

                # 화면이 회색으로 바뀐다.
                displaysurface.fill(GRAY)
                
                # game_over 변수에 저장된 GAME OVER 문구를 해당 위치에 출력
                displaysurface.blit(game_over, (30, 250))
                
                # 게임종료 화면에서 최종 스코어 출력
                total_score = font_small.render(f'Score :  {P1.score}', True, BLACK)
                displaysurface.blit(total_score, (30, 350))

                # 하이스코어를 갱신 했을 경우
                if P1.score > int(highscore):
                    highscore = P1.score
                    # 작성하기('w')로 open 시 안에 내용 다 지워짐
                    f = open(HS_FILE, 'w')
                    # P1.score 의 값을 저장하고
                    f.write(str(P1.score))
                    f.close()
                # 게임오버 화면에 하이스코어 출력
                highscore_out = font_small.render(f'HighScore : {highscore}', True, BLACK)
                displaysurface.blit(highscore_out, (30, 450))

                pygame.display.update() #Game Over 화면 출력
                time.sleep(5) # 5초뒤
                pygame.quit() # 꺼짐
                sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
