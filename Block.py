import pygame, sys
import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as tkMessageBox
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
class Block(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.type = 'Block'

        self.Font = pygame.font.SysFont('bahnschrift', 20)
        self.SmallFont = pygame.font.SysFont('bahnschrift', 14)
        self.colors = {'black': (0, 0, 0), 'blue': (26, 27, 250)}

        self.width = 120
        self.height = 80

        self.current_width = 0
        self.current_height = 0

        self.color = self.colors['black']

        self.highlighted = False
        self.drag = False

        self.name = "G(s)"

        self.actual_num = []
        self.actual_den = []
        self.last_num = []
        self.last_den = []
        self.rendered_num = ""
        self.rendered_den = ""
        self.rendered_num_exponents = ""
        self.rendered_den_exponents = ""

        self.rect = pygame.Rect(10, 10, self.width, self.height)
#-------------------------------------------------------------------------
    def Draw(self, screen):
        #-------------------------------------------------------------------------
        def Render_Coefficients(coefficient_lists):

            rendered_coefficients = []

            for coefficients in coefficient_lists:
                buffer_text = []

                for i in range(len(coefficients)):

                  if coefficients[i] > 0:
                    if i == 0:
                      buffer_text.append(str(coefficients[i]) + "s")
                    elif i == len(coefficients)-1:
                      buffer_text.append("+ " + str(coefficients[i]))
                    else:
                      buffer_text.append("+ " + str(coefficients[i]) + "s")

                  else:
                    if i == 0:
                      buffer_text.append("- " + str(coefficients[i])[1:] + "s")
                    elif i == len(coefficients)-1:
                      buffer_text.append("- " + str(coefficients[i])[1:])
                    else:
                      buffer_text.append("- " + str(coefficients[i])[1:] + "s")

                rendered_text = " ".join(x for x in buffer_text)
                rendered_coefficients.append(rendered_text)

            return rendered_coefficients
        #-------------------------------------------------------------------------
        def Render_Exponents(rendered_coefficients):

            rendered_exponents = []

            for coefficients in rendered_coefficients:
                exponents = ""
                if rendered_coefficients.index(coefficients) == 0:
                    degree = len(self.actual_num) - 1
                else:
                    degree = len(self.actual_den) - 1

                for item in range(len(coefficients)):

                    if item == 0:
                        exponents += 2*' '
                    else:
                        if coefficients[item-1] == 's':
                            if degree == 1:
                                exponents += 2*' '
                            else:
                                exponents += 1*' '+str(degree)
                                degree -= 1
                        else:
                            exponents += 2*' '
                rendered_exponents.append(exponents)

            return rendered_exponents
        #-------------------------------------------------------------------------
        if self.highlighted:
            self.color = self.colors['blue']
        else:
            self.color = self.colors['black']

        if len(self.actual_num)==0 and len(self.actual_den)==0:
            text = self.Font.render(self.name, True, self.color)
            text_width = text.get_width()
            text_height = text.get_height()

            self.current_width = self.rect.right - self.rect.left
            self.rect.inflate_ip(self.width-self.current_width, 0)

            text_x = self.rect.center[0] - text_width//2
            text_y = self.rect.center[1] - text_height//2
            text_coordinates = (text_x, text_y)
            screen.blit(text, text_coordinates)
        else:

            if self.actual_num != self.last_num or self.actual_den != self.last_den:
                rendered_coefficients = Render_Coefficients([self.actual_num, self.actual_den])
                self.rendered_num = rendered_coefficients[0]
                self.rendered_den = rendered_coefficients[1]
                rendered_exponents = Render_Exponents([self.rendered_num, self.rendered_den])
                self.rendered_num_exponents = rendered_exponents[0]
                self.rendered_den_exponents = rendered_exponents[1]
            else:
                pass

            num_text = self.Font.render(self.rendered_num, True, self.color)
            num_text_width = num_text.get_width()
            num_text_height = num_text.get_height()

            den_text = self.Font.render(self.rendered_den, True, self.color)
            den_text_width = den_text.get_width()
            den_text_height = den_text.get_height()

            num_exp_text = self.SmallFont.render(self.rendered_num_exponents, True, self.color)
            num_exp_text_width = num_exp_text.get_width()
            num_exp_text_height = num_exp_text.get_height()

            den_exp_text = self.SmallFont.render(self.rendered_den_exponents, True, self.color)
            den_exp_text_width = den_exp_text.get_width()
            den_exp_text_height = den_exp_text.get_height()


            if num_text_width > den_text_width:
                max_text_lenght = num_text_width
            else:
                max_text_lenght = den_text_width

            self.current_width = self.rect.right - self.rect.left
            self.current_height = self.rect.bottom - self.rect.top


            self.rect.inflate_ip(max_text_lenght-self.current_width+5, 0)


            num_text_x = self.rect.center[0] - num_text_width//2
            num_text_y = self.rect.center[1] - self.current_height//4 - num_text_height//2
            num_text_coordinates = (num_text_x, num_text_y)
            screen.blit(num_text, num_text_coordinates)

            den_text_x = self.rect.center[0] - den_text_width//2
            den_text_y = self.rect.center[1] + self.current_height//4 - den_text_height//2
            den_text_coordinates = (den_text_x, den_text_y)
            screen.blit(den_text, den_text_coordinates)

            num_exp_text_x = self.rect.center[0] - num_text_width//2
            num_exp_text_y = self.rect.center[1] - 3*self.current_height//8 - num_exp_text_height//2
            num_exp_text_coordinates = (num_exp_text_x, num_exp_text_y)
            screen.blit(num_exp_text, num_exp_text_coordinates)

            den_exp_text_x = self.rect.center[0] - den_text_width//2
            den_exp_text_y = self.rect.center[1] + 1*self.current_height//8 - den_exp_text_height//2
            den_exp_text_coordinates = (den_exp_text_x, den_exp_text_y)
            screen.blit(den_exp_text, den_exp_text_coordinates)

            line_start_pos = (self.rect.center[0]-max_text_lenght//2, self.rect.center[1])
            line_end_pos = (self.rect.center[0]+max_text_lenght//2, self.rect.center[1])
            pygame.draw.line(screen, self.color, line_start_pos, line_end_pos)



        pygame.draw.rect(screen, self.color, self.rect, 1)
#-------------------------------------------------------------------------
    def Edit_Coefficients(self):
        #-------------------------------------------------------------------------
        def Obtain_Coefficients():

            num_text = Numerator_Input.get().split(" ")
            den_text = Denominator_Input.get().split(" ")
            num = []
            den = []
            errors = False

            for number in num_text:
                try:
                    coefficient= float(number)
                except:
                    tkMessageBox.showerror("Error Message", "COEFFICIENT ERROR\nPlease enter valid coefficients")
                    print("Appending error [num]")
                    errors = True
                    break
                if coefficient- int(coefficient) !=0:
                    num.append(coefficient)
                else:
                    num.append(int(coefficient))

            for number in den_text:
                try:
                    coefficient= float(number)
                except:
                    tkMessageBox.showerror("Error Message", "COEFFICIENT ERROR\nPlease enter valid coefficients")
                    print("Appending error [den]")
                    errors = True
                    break
                if coefficient- int(coefficient) !=0:
                    den.append(coefficient)
                else:
                    den.append(int(coefficient))

            self.last_num = self.actual_num
            self.last_den = self.actual_den
            self.actual_num = num
            self.actual_den = den
            print("Num: ", self.actual_num)
            print("Den: ", self.actual_den)

            if not errors:
                print("No errors")
                main_window.destroy()
        #-------------------------------------------------------------------------

        main_window = tk.Tk()
        main_window.title("Set Coefficients  -  {}".format(self.name))
        main_window.geometry('300x200')

        fontStyle = tkFont.Font(family="Bahnschrift Light", size=12)

        global Numerator_Input, Denominator_Input

        Numerator_Input = tk.Entry(main_window, width=30, font=fontStyle, justify='center')
        Numerator_Input.insert(0, ' '.join(str(coefficient) for coefficient in self.actual_num))
        Numerator_Input.place(x=150, y=50, anchor='center')

        label_numerator = tk.Label(main_window, text="Numerator: ", font=fontStyle)
        label_numerator.place(x=150, y=25, anchor='center')


        Denominator_Input = tk.Entry(main_window, width=30, font=fontStyle, justify='center')
        Denominator_Input.insert(0, ' '.join(str(coefficient) for coefficient in self.actual_den))
        Denominator_Input.place(x=150, y=120, anchor='center')

        label_denominator = tk.Label(main_window, text="Denominator: ", font=fontStyle)
        label_denominator.place(x=150, y=95, anchor='center')

        button_Send = tk.Button(main_window, text='Set Transfer Function', width=20, font=fontStyle, command=Obtain_Coefficients)
        button_Send.place(x=150, y=170, anchor='center')

        main_window.mainloop()
#-------------------------------------------------------------------------
