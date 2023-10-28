#this imports the relevant libraries to the program.
import tkinter
import tkintermapview
import math

#this gets the users screen size, so the map is the same ratio size
import ctypes
user32 = ctypes.windll.user32
screensizex = str(user32.GetSystemMetrics(0))
screensizey = str(user32.GetSystemMetrics(1))
screensize = screensizex+"x"+screensizey

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        #configuring the window
        self.title("Nuclear fallout Simulator")
        self.geometry(screensize)

        #setting up label for explosive value input prompt
        self.explosive_value_label = tkinter.Label(text="Enter your explosive value, in kilotones, between 1t(0.01) and 100Mt(100,000Kt) equivilant")
        self.explosive_value_label.grid(row = 0, column = 0)

        #setting up the quit button
        self.quit_button = tkinter.Button(self, text = "Quit", fg = "red", command = quit)
        self.quit_button.grid(row = 2, column = 1)

        
        #setting up entry slot of explosive value
        self.explosive_value_submittion = tkinter.Entry(self)
        self.explosive_value_submittion.grid(row = 1,column = 0)

        #setting up exposive value submit button &validdation
        validation = validate_data()
        self.explosive_value_submit_button = tkinter.Button(self, text="Submit", command = lambda:validation.validate(self.explosive_value_submittion))
        self.explosive_value_submit_button.grid(row=2, column = 0)
        
        #this is setting up the initial values for the map in this program.
        self.the_map = tkintermapview.TkinterMapView(self, width=int(screensizex)*3/4, height=int(screensizey)*8/10, corner_radius=0)
        self.the_map.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.the_map.set_position(51.51279, -0.09184)
        self.the_map.set_zoom(12)

        #this it to create a map marker, which will bbe used as the position of the nukes that are placed.
        def add_marker_event(coords):
            self.new_marker = self.the_map.set_marker(coords[0], coords[1], text = "Nuke")

        self.the_map.add_right_click_menu_command(label = "Place nuke", command= add_marker_event,pass_coords = True)

    def give_explosive_size(self):
        return self.exposive_value_submittion.get()
    


class validate_data():

    def __init__(self):
        self.program_ran = False
        self.radius_report_label = tkinter.Label(text = "")
        self.radius_report_label.grid(row = 3, column = 1)
        self.report_label_explosive_input_validity = tkinter.Label(text = "")
        self.report_label_explosive_input_validity.grid(row = 3, column = 0)

    #this section of code takes an input and determines whether it is a float, by using a try function, and returning True if it can be a float, and false if it cant    
    def is_float(explosion):
       try:
           float(explosion)
           return True
       except ValueError:
           return False
       
    

    def validate(self,explosive_value_submittion):
        #this code gets the input from the user and assigns it to the variable tnt_equivilent for use in the validation of the program
        tnt_equivilent = explosive_value_submittion.get()
        #this is the beginning of the validation of the program, limiting the amount of chrarcters that can be used for the input
        if len(tnt_equivilent) < 20:
            #this checks to make sure the user input is either a float or  integer, and then if it is, converts the variable to a float
            if validate_data.is_float(tnt_equivilent) == True or tnt_equivilent.isnumeric() == True:
                tnt_equivilent = float(tnt_equivilent)
                #here the program checks to see whether the input is in the accepted range of values
                if tnt_equivilent>= 0.01 and tnt_equivilent <= 1000000.0:
                    if self.program_ran == False:
                        #this reports that the input was valid, the may be removed in later versions
                        self.report_label_explosive_input_validity.config(text="Valid Input", fg = "black")
                        #this sends through the size of the explosive and gets the calclated radius from that value
                        radius_of_the_explosion = radius_of_Explosion(tnt_equivilent)
                        radius_of_the_explosion = radius_of_the_explosion.calculate_radius()
                        #this function outputs the radius of the explosion to 4 decimal places
                        self.radius_report_label.config(text = "Radius of explosion: "+str(round(radius_of_the_explosion,4))+"m")
                        self.program_ran = True
                    else:
                        self.report_label_explosive_input_validity.config(text="Valid input", fg = "black")
                        #this sends through the size of the explosive and gets the calclated radius from that value
                        radius_of_the_explosion = radius_of_Explosion(tnt_equivilent)
                        radius_of_the_explosion = radius_of_the_explosion.calculate_radius()
                        #this function outputs the radius of the explosion to 4 decimal places
                        self.radius_report_label.config(text ="Radius of explosion: "+str(round(radius_of_the_explosion,4))+"m")
                        
                #if the tnt_equivilent isnt within range it gives this output, and blanks the radius label if its been used
                else:
                    if self.program_ran == False:
                        self. report_label_explosive_input_validity.config(text="Invalid input, please enter a number in the range.", fg = "red")
                        self.radius_report_label.config(text = " ", fg = "black")
                        self.program_ran = True
                    else:
                        self.report_label_explosive_input_validity.config(text="Invalid input, please enter a number in the range.", fg = "red")
                        self.radius_report_label.config(text = " ", fg = "black")

            #this is used when a number in integer or float form isnt used and gives the the messages below, as well as blanking the radius report label                 
            else:
                if self.program_ran == False:
                    self.report_label_explosive_input_validity.config(text="Invalid input, please enter a number.", fg = "red")
                    self.radius_report_label.config(text=" ", fg = "black")
                    self.program_ran = True
                else:
                    self.report_label_explosive_input_validity.config(text="Invalid input, please enter a number.", fg = "red")
                    self.radius_report_label.config(text = " ", fg = "black")

        #this is used when the number is too long,and will also blank radius report
        else:
            if self.program_ran == False:
                self.report_label_explosive_input_validity.config(text="Invalid input, please enter a number between less than 20 characters long.", fg = "red")
                self.radius_report_label = tkinter.Label(text=" ", fg = "black")
                self.program_ran = True
            else:
                self.report_label_explosive_input_validity.config(text="Invalid input, please enter a number between less than 20 characters long.", fg = "red")
                self.radius_report_label.config(text = " ", fg = "black")

class radius_of_Explosion(App):
    #this is also used to find the to find the radius, it is the density of air in kgm^-3
    air_density = 1.293

    #this is used in the equation to find the radius of the explosion, it is measuered in secounds is the average time for a nuclear explosion to get to its maxiumum size
    time_of_blast = 0.00000008
    
    def __init__(self,tnt_equivilent):
        #this is getting the explosive value of the blast, it will be later converted into rough energy for the equation
        self.explosive_value = tnt_equivilent

    def calculate_radius(self):
        #4.184*10^9, is in joules the amount of energy stored in 1 metric tonne of TNT
        energy = (math.pow(4.184*10,9))*self.explosive_value
        radius = (energy**(1/5))*(self.time_of_blast**(2/5))*(self.air_density**(-1/5))
        return radius

if __name__ == "__main__":
    app = App()
    app.mainloop())
