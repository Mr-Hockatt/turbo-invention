import pygame,sys
import tkinter as tk
import tkinter.font as tkFont
#------------------------------------------------------------------
pygame.init()
clock = pygame.time.Clock()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Block Class")
#------------------------------------------------------------------
def Interfaz():
    main_window = tk.Tk()
    main_window.title("Set Transfer Function")
    main_window.geometry('300x200')
    #main_window.configure(bg='white')
    fontStyle = tkFont.Font(family="Bahnschrift Light", size=12)

    global Numerator_Input, Denominator_Input
    Numerator_Input = tk.Entry(main_window, width=30, font=fontStyle, justify='center')
    Numerator_Input.place(x=150, y=50, anchor='center')

    label_numerator = tk.Label(main_window, text="Numerator: ", font=fontStyle)
    label_numerator.place(x=150, y=25, anchor='center')


    Numerator_Input = tk.Entry(main_window, width=30, font=fontStyle, justify='center')
    Numerator_Input.place(x=150, y=120, anchor='center')

    label_numerator = tk.Label(main_window, text="Denominator: ", font=fontStyle)
    label_numerator.place(x=150, y=95, anchor='center')

    button_Send = tk.Button(main_window, text='Set Transfer Function', width=20, font=fontStyle, command= lambda: print("Working Button :3"))
    button_Send.place(x=150, y=170, anchor='center')

    main_window.mainloop()
#------------------------------------------------------------------
black = (0, 0, 0)
white = (255, 255, 255)
#blue = (22, 222, 175)
blue = (26, 27, 250)

block_w = 140
block_h = 80
block = pygame.Rect(screen_width//2, screen_height//2, block_w, block_h)
highlighted = False
drag = False


Font = pygame.font.SysFont('bahnschrift', 28)


def Draw_Block():

    if highlighted:
        block_color = blue
        block_text_color = blue
    else:
        block_color = black
        block_text_color = black

    #if drag:
    #    block.center = mouse

    block_text = Font.render("G(s)", True, block_text_color)
    block_text_width = block_text.get_width()
    block_text_height = block_text.get_height()
    block_text_x = block.center[0] - block_text_width//2
    block_text_y = block.center[1] - block_text_height//2
    block_text_coordinates = (block_text_x, block_text_y)

    pygame.draw.rect(screen, block_color, block, 1)
    screen.blit(block_text, block_text_coordinates)



#------------------------------------------------------------------
while True:
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()


    if block.right>mouse[0]>block.left and block.bottom>mouse[1]>block.top:

        if click[0]:
            print("Block Selected")
            highlighted = True
        elif click[2]:
            print("Right Click")
            block.inflate_ip(2,2)
            print(block.top-block.bottom, block.right-block.left)
    else:
        if click[0]:
            highlighted = False
            print("Block Unselected")


    #Event Handling
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if block.collidepoint(mouse):
                    drag = True

        if event.type == pygame.MOUSEBUTTONUP:
            drag = False

        if event.type == pygame.MOUSEMOTION:
            if drag:
                block.center = mouse

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if highlighted:
                    print("Ready to select transfer function")
                    Interfaz()

    #Visuals
    screen.fill(white)

    Draw_Block()


    #Window Update
    pygame.display.update()
    clock.tick(60)
#------------------------------------------------------------------
