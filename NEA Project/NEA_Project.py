import tkinter
import tkintermapview
import math


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()



        #configuring the window
        self.title("Nuclear fallout Simulator")
        self.geometry("2256x1504")

        #setting up label for explosive value input prompt
        self.explosive_value_label = tkinter.Label(text="Enter your explosive value, in kilotones, between 1t(0.01) and 100Mt(100,000Kt) equivilant")
        self.explosive_value_label.grid(row = 0, column = 0)

        #setting up the quit button
        self.quit_button = tkinter.Button(self, text = "Quit", fg = "red", command = quit)
        self.quit_button.grid(row = 2, column = 1)

        
        #setting up entry slot of explosive value
        self.explosive_value_submittion = tkinter.Entry(self)
        self.explosive_value_submittion.grid(row = 1,column = 0)

        #setting up exposive value submit button
        self.explosive_value_submit_button = tkinter.Button(self, text="Submit", command = validate_data.validate(self,self.explosive_value_submittion))
        self.explosive_value_submit_button.grid(row=2, column = 0)
        
        #this is setting up the initial values for the map in this program.
        self.the_map = tkintermapview.TkinterMapView(self, width=1600, height=1000, corner_radius=0)
        self.the_map.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.the_map.set_position(51.51279, -0.09184)
        self.the_map.set_zoom(12)

        
        def add_marker_event(coords):
            self.new_marker = self.the_map.set_marker(coords[0], coords[1], text = "Nuke")

        self.the_map.add_right_click_menu_command(label = "Place nuke", command= add_marker_event,pass_coords = True)

    def give_explosive_size(self):
        return self.exposive_value_submittion.get()


class validate_data(App):
    def __init__(self):
        super().__init__()

        
    def is_float(self,explosion):
       try:
           float(explosion)
           return True
       except ValueError:
           return False


    def validate(self,explosive_value_submittion):
        explosion = explosive_value_submittion.get()
        if len(explosion) < 20:
                if validate_data.is_float(self,explosion) == True or explosion.isnumeric() == True:
                    explosion = float(explosion)
                    if explosion>= 0.01 and explosion <= 1000000.0:
                        self.report_label_explosive_input_validity = tkinter.Label("Valid input")
                        self.report_label_explosive_input_validity.grid(row=3,column=0)
                    else:
                        self.report_label_explosive_input_validity = tkinter.Label(text="Invalid input, please enter a number in the range.", fg = "red")
                        self.report_label_explosive_input_validity.grid(row = 3, column = 0)
                else:
                     self.report_label_explosive_input_validity = tkinter.Label(text="Invalid input, please enter a number.", fg = "red")
                     self.report_label_explosive_input_validity.grid(row = 3, column = 0)
        else:
             self.report_label_explosive_input_validity = tkinter.Label(text="Invalid input, please enter a number between less than 20 characters long.", fg = "red")
             self.report_callback_exception.grid(row = 3, column = 0)


class radius_of_Explosion(App):
    def __init__(self):
        #this is getting the explosive value of the blast, it will be later converted into rough energy for the equation
        self.explosive_value = 0
        self.explosive_value = self.exposive_value.get_expolsive_size()
        #this is used in the equation to find the radius of the explosion, it is measuered in secounds is the average time for a nuclear explosion to get to its maxiumum size
        self.time_of_blast = 0.00000008
        #this is also used to find the to find the radius, it is the density of air in kgm^-3
        self.air_density = 1.293

    def calculate_radius(self):
        #4.184*10^9, is in joules the amount of energy stored in 1 metric tonne of TNT
        self.energy = (4.184*10^9)*self.explosive_value

        self.radius = (self.energy^(1/5) )*(self.time_of_blast^(2/5))*(self.air_density^(-1/5))
        return self.radius

if __name__ == "__main__":
    app = App()
    app.mainloop()