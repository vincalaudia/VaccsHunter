import pygame,sys,random
pygame.init()

def woman_animation():
	new_woman = woman_frames[woman_index]
	new_woman_rect = new_woman.get_rect(center = (150,woman_rect.centery))
	return new_woman,new_woman_rect

def draw_floor():
	SCREEN.blit(bg,(bg_x_pos,0)) 
	SCREEN.blit(bg,(bg_x_pos + 1600,0))

def create_cov():
    random_length = random.choice(cov_length)
    random_cov_pos = random.choice(cov_height)
    bottom_cov = cov_surface.get_rect(midtop = (random_length,random_cov_pos))
    top_cov = cov_surface.get_rect(midbottom = (random_length,random_cov_pos +15))
    return bottom_cov,top_cov

def draw_covs(covs):
	for cov in covs:
		if cov.bottom >= 512:
			SCREEN.blit(cov_surface,cov)
		else:
			flip_cov = pygame.transform.flip(cov_surface,False,True)
			SCREEN.blit(flip_cov,cov)

def move_covs(covs):
    oh = 3
    for cov in covs:
        cov.centerx -= oh
        oh+=0.5
    visible_covs = [cov for cov in covs if cov.right > -25]
    return visible_covs

def check_collision(covs):
    global can_score
    for cov in covs:
        if woman_rect.colliderect(cov):
            #soundeffect game over
            gameover.play()
            can_score = True
            return False

    if woman_rect.top <= 250 or woman_rect.bottom >= 500:
        #soundeffect game over
        gameover.play()
        can_score = True
        return False

    return True

#Display Score
score=0
high_score=0
game_font = pygame.font.Font('stick.ttf',20)
def score_display():
    if start:
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (400,30))
        SCREEN.blit(score_surface,score_rect)
    else:
        score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
        score_rect = score_surface.get_rect(center = (400,30))
        SCREEN.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (400,450))
        SCREEN.blit(high_score_surface,high_score_rect)

#Add Score
can_score=True
def cov_score_check():
    global score, can_score 
    
    if cov_list:
        for cov in cov_list:
            if 45 < cov.centerx < 50 and can_score:
                score += 1
                #sound point
                point.play()
                can_score = False
            if cov.centerx < 0:
                can_score = True

SCREEN = pygame.display.set_mode((800,500))
pygame.display.set_caption("Vaccs Hunter")
clock = pygame.time.Clock()
FPS = 120

init_surface = pygame.image.load('assets/Immune.png').convert_alpha()
init_rect = init_surface.get_rect(center = (400,250))

bg = pygame.image.load('assets/po.png').convert()
sprite_stand = pygame.image.load('assets/spritestand.png').convert_alpha()
sprite_walk1 = pygame.image.load('assets/spritewalk1.png').convert_alpha()
spritewalk2 = pygame.image.load('assets/spritewalk2.png').convert_alpha()
woman_frames = [sprite_stand,sprite_walk1,spritewalk2]
woman_index = 0
woman_surface = woman_frames[woman_index]
woman_rect = woman_surface.get_rect(center = (150,390))

walk = pygame.mixer.Sound('sound/walk.wav')
gameover = pygame.mixer.Sound('sound/gameover.wav')
point = pygame.mixer.Sound('sound/point.wav')

cov_surface = pygame.image.load('assets/corona.png').convert()
cov_height = [335, 445, 390]
cov_length = [800, 900]

SPAWNcov = pygame.USEREVENT + 1 # Buat event dengan USEREVENT + 1
pygame.time.set_timer(SPAWNcov,2000) 
cov_list= [] # Siapkan list kosong untuk pipa yang akan dibuat

womanWALK = pygame.USEREVENT
pygame.time.set_timer(womanWALK,200)

bg_x_pos = 0
cov_surface = pygame.image.load('assets/corona.png').convert()
cov_list=create_cov()

start = False
woman_movement = 0
gravity = 0.1

SCREEN.blit(bg,(0,0))


#mulai
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        clicked =False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE and not start: 
                start = True
            if event.key == pygame.K_UP and start:
                woman_rect.centery += -55
                walk.play()
            if event.key == pygame.K_DOWN and start:
                woman_rect.centery += 55
                walk.play()
            
        if event.type == womanWALK:
            if woman_index < 2:
                woman_index += 1
            else:
                woman_index = 0
            woman_surface, woman_rect = woman_animation()

        if event.type == SPAWNcov:
            cov_list= []
            for i in range(2) :
                cov_list.extend(create_cov())
                pass
       

        if clicked and start:
            woman_movement = -5               
            

        if event.type == womanWALK:
            if woman_index < 2:
                woman_index += 1
            else:
                woman_index = 0

    if start :
        SCREEN.blit(bg,(0,0))
        bg_x_pos -= 3
        draw_floor()
        if bg_x_pos <= -1600:
            bg_x_pos = 0

    if start:
        SCREEN.blit(woman_surface, woman_rect)
        cov_list = move_covs(cov_list)
        draw_covs(cov_list)
         
    else:
        SCREEN.blit(sprite_stand, woman_rect)
    
    if start: 
        
        woman_rect.centery += woman_movement
        SCREEN.blit(woman_surface,woman_rect)
       
       ##########__________________________________________________ slide 13
        # Collision dicek dari awal tiap frame pada tiap pipa (cov_list) yang dibuat
        
        #STEP 2: apply the function here
        # it will make the start false if there is a collision
        start = check_collision(cov_list)
        # END STEP 2
 
        ####### ______________________________ HIGH SCORE _______________________ Slide 15
        # 4 if game over update the highscore
        # Setelah terjadi collision, score yang diperoleh kita bandingkan dengan high score sebelumnya, 
        # dan jika score sekarang lebih baik, simpan score tadi menjadi high score yang baru
        if not start:
            if high_score<score:
                high_score=score
        # END 4
        
        #### ___________________________ ADD SCORE __________________________________SLIDE 8
        cov_list = move_covs(cov_list)
        draw_covs(cov_list)
        #Step 7 : always check the score every frame
        cov_score_check()
        #END step 7
        
    else:
       
        #### _________________________ Slide 18 ___________________________
        #2 if not start we render the init surface instead
        # SCREEN.blit(woman_downWALK,woman_rect)
        SCREEN.blit(init_surface,init_rect)
        woman_rect = woman_surface.get_rect(center = (150,390))
        start=False
        cov_list= [] 
        

        if start :
            woman_index = 0
            woman_surface = woman_frames[woman_index]
            score=0
          
            
      
    
    
    # Menampilkan score dan high score dengan fungsi score_display() dilakukan di akhir permainan, tepatnya sebelum display update 
    score_display()
    
    
    pygame.display.update()
