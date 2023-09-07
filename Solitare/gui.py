import pygame 
import random

pygame.init()

#windows
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Test")

#rect = image.get_rect()

def obraz():
    screen.blit(image, (x,y))

# rect.center = (350, 350)
boxes = []
active_box = None
# pygame.Surface.blit(image, rect)

box = pygame.Rect(10,10,100,100)
boxes.append(box)

cards = []   
active_card = None 
for i in range(1, 7):
        image = pygame.image.load(f"cards/Pik{str(i)}.png")
        x = 100*i
        y = 250
        card = screen.blit(image, (x,y))
        cards.append(card)

run = True
while run:    

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for id, card in enumerate(cards):
                    if card.collidepoint(event.pos):
                        active_card = id
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_card = None

        if event.type == pygame.MOUSEMOTION:
            if active_card != None:
                print(cards[active_card])
                cards[active_card].move_ip(event.rel)

    # for event in pygame.event.get():
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         if event.button == 1:
    #             for num, box in enumerate(boxes):
    #                 if box.collidepoint(event.pos):
    #                     active_box = num
    #     if event.type == pygame.MOUSEBUTTONUP:
    #         if event.button == 1:
    #             active_box = None

    #     if event.type == pygame.MOUSEMOTION:
    #         if active_box != None:
    #             boxes[active_box].move_ip(event.rel)


        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()



pygame.quit()