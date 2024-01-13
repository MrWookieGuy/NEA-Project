##this imports the relevant libraries to the program.
#note the 1st library was automatically put in to make null a vaild data
from asyncio.windows_events import NULL
from pickle import NONE
import tkinter
import tkintermapview
import math
import csv
#from google import Translator

#this gets the users screen size, so the map is the same ratio size
import ctypes
user32 = ctypes.windll.user32
screensizex = str(user32.GetSystemMetrics(0))
screensizey = str(user32.GetSystemMetrics(1))
screensize = screensizex+"x"+screensizey

#These are all the global variables in the program
area_of_effect = NULL
marker_placed = False
centre_coords = NULL
the_map = NULL

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        #configuring the window
        self.title("Nuclear fallout Simulator")
        self.geometry(screensize)

        #setting up label for explosive value input prompt
        self.explosive_value_label = tkinter.Label(text="Enter your explosive value, in kilotones, between 1t(0.01) and 100Mt(100,000,000Kt) equivilant")
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
        global the_map 
        the_map = tkintermapview.TkinterMapView(self, width=int(screensizex)*3/4, height=int(screensizey)*8/10, corner_radius=0)
        the_map.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        the_map.set_position(51.51279, -0.09184)
        the_map.set_zoom(12)

        #this it to create a map marker, which will be used as the position of the nukes that are placed.
        def add_marker_event(coords):
            global marker_placed
            global the_map
            if marker_placed == False:    
                self.new_marker = the_map.set_marker(coords[0], coords[1], text = "Nuke")
                global centre_coords
                centre_coords = coords
                marker_placed = True
            else:
                pass
                
        
        the_map.add_right_click_menu_command(label = "Place nuke", command= add_marker_event,pass_coords = True)

        def give_explosive_size(self):
             return self.exposive_value_submittion.get()


        #this it the process to reset the map if you rightclick and then choose reset map
        def reset_map(self):
            global the_map
            global marker_placed
            global area_of_effect
            self.new_marker.delete()
            area_of_effect.delete()
            marker_placed = False           
            
        the_map.add_right_click_menu_command(label = "Clear map", command = lambda:reset_map(self))
    


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
                if tnt_equivilent>= 0.01 and tnt_equivilent <= 100000000.0:
                    if self.program_ran == False:
                        #this reports that the input was valid, the may be removed in later versions
                        self.report_label_explosive_input_validity.config(text="Valid Input", fg = "black")
                        #this sends through the size of the explosive and gets the calclated radius from that value
                        radius_of_the_explosion = radius_of_Explosion(tnt_equivilent)
                        radius_of_the_explosion = radius_of_the_explosion.calculate_radius()
                        
                        #this section if defining and then drawing the area of effect onto the map
                        if marker_placed == True:
                            global centre_coords
                            global the_map
                            area_of_effect = draw_area_of_effect(radius_of_the_explosion,centre_coords)
                            area_of_effect.defining_path()
                            area_of_effect.creating_area_of_effect_display(the_map)
                        

                        #this function outputs the radius of the explosion to 4 decimal places
                        self.radius_report_label.config(text = "Radius of explosion: "+str(round(radius_of_the_explosion,4))+"m")
                        self.program_ran = True
                     
                    #this else statement is used when the program has been run more than one time, and the input is valid, it performs the same functions as above, and in the same fashion
                    else:
                        self.report_label_explosive_input_validity.config(text="Valid input", fg = "black")
                        
                        #this sends through the size of the explosive and gets the calclated radius from that value
                        radius_of_the_explosion = radius_of_Explosion(tnt_equivilent)
                        radius_of_the_explosion = radius_of_the_explosion.calculate_radius()
                        
                        #this function outputs the radius of the explosion to 4 decimal places
                        self.radius_report_label.config(text ="Radius of explosion: "+str(round(radius_of_the_explosion,4))+"m")
                        if marker_placed == True:
                            area_of_effect = draw_area_of_effect(radius_of_the_explosion,centre_coords)
                            area_of_effect.defining_path()
                            area_of_effect.creating_area_of_effect_display(the_map)
                        
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
    time_of_blast = 3.5
    
    def __init__(self,tnt_equivilent):
        #this is getting the explosive value of the blast, it will be later converted into rough energy for the equation
        self.explosive_value = tnt_equivilent

    def calculate_radius(self):
        #4.184*10^9, is in joules the amount of energy stored in 1 metric tonne of TNT
        energy = (4.184*(10**9))*self.explosive_value*1000
        energy = energy**(1/5)
        self.time_of_blast = self.time_of_blast**(2/5)
        self.air_density = self.air_density**(-1/5)
        radius = energy*self.time_of_blast*self.air_density
        return radius
    
class draw_area_of_effect(App):
    
    def __init__(self,radius,coordinates):
        #this defines the parameters of the class, these being the array of points around the area of effect, the radius of the explosion, converted into change in decimal coordinates
        self.array_of_points = [[]]
        self.radius_of_the_explosion = int(radius)/111000
        self.coordinates_of_explosion_x = coordinates[1]
        self.coordinates_of_explosion_y = coordinates[0]
       
    def defining_path(self):
        #this method creates an array, with tuples of the points on the "circle"
        self.array_of_points[0] = [self.coordinates_of_explosion_y+self.radius_of_the_explosion, self.coordinates_of_explosion_x]

        #these for statements are making 6 points for each quarter of the side, the comment before states which sector it is. the appendages on their own are for when 
        #+y, +x
        for side_number in range (0,6):
            change_in_x = math.cos((math.pi/12)*(4-side_number+1))*self.radius_of_the_explosion
            change_in_y = math.sin((math.pi/12)*(4-side_number+1))*self.radius_of_the_explosion
            new_element = [self.coordinates_of_explosion_y+change_in_y,self.coordinates_of_explosion_x+change_in_x]
            self.array_of_points.append(new_element)
           
        self.array_of_points[6] = [self.coordinates_of_explosion_y,self.coordinates_of_explosion_x+self.radius_of_the_explosion]

        #-y, +x
        for side_number in range (0,6):
            change_in_x = math.cos((math.pi/12)*(side_number+1))*self.radius_of_the_explosion
            change_in_y = math.sin((math.pi/12)*(side_number+1))*self.radius_of_the_explosion
            new_element = [self.coordinates_of_explosion_y-change_in_y,self.coordinates_of_explosion_x+change_in_x]
            self.array_of_points.append(new_element)
        
        self.array_of_points[12] = [self.coordinates_of_explosion_y-self.radius_of_the_explosion,self.coordinates_of_explosion_x]
       
        #-y, -x
        for side_number in range (0,6):
            change_in_x = math.cos((math.pi/12)*(4-side_number+1))*self.radius_of_the_explosion
            change_in_y = math.sin((math.pi/12)*(4-side_number+1))*self.radius_of_the_explosion
            new_element = [self.coordinates_of_explosion_y-change_in_y,self.coordinates_of_explosion_x-change_in_x]
            self.array_of_points.append(new_element)

        self.array_of_points[18] = [self.coordinates_of_explosion_y,self.coordinates_of_explosion_x-self.radius_of_the_explosion]

        #+y, -x
        for side_number in range (0,6):
            change_in_x = math.cos((math.pi/12)*(side_number+1))*self.radius_of_the_explosion
            change_in_y = math.sin((math.pi/12)*(side_number+1))*self.radius_of_the_explosion
            new_element = [self.coordinates_of_explosion_y+change_in_y,self.coordinates_of_explosion_x-change_in_x]
            self.array_of_points.append(new_element)
        #this print statement is here to allow for easier debugging if errors occur with the layout of the circle.
        print(self.array_of_points)
           
    def creating_area_of_effect_display(self,the_map):
        global area_of_effect
        area_of_effect = the_map.set_path(self.array_of_points)
        

class casulty_count_calculation_and_display():
    #this instantieates the variables that will be used in this section of the program
    def __init__(self,radius):
        self.area_of_country = NULL
        self.population_of_country = NULL
        self.population_density_of_country = NULL
        self.fields = []
        self.rows = []
        self.area_effected = radius**2*math.pi
        self.row_of_country = NONE
        self.causlty_count_label = tkinter.Label("")
        self.causlty_count_label.grid(0,3)
        
        
    def retrieve_data_from_csv(self):
        #this sets the a varible to the name of the file, so it doesn't have to be writen many times
        filename = "pop density.csv"
        
        #reading the csv file
        with open(filename, "r") as csvfile:
            #this part is creating a csv reader object, from the csv library
            csvreader = csv.reader(csvfile)
            #this is getting the fields of the csv file from the file
            self.fields = next(csvreader)
            #this is getting the dat from all of the rows one by one
            for row in csvreader:
                self.rows.append(row)

        
    def get_country_data(self):
        #this program gets the country which the arrow is in, it then uses a linear searchto find the country in the csv file. this is done after translating the country to english
        global centre_coords
        country = tkintermapview.convert_coordinates_to_country(centre_coords)
        translator = Translator()
        country = translator.translate(country)
        search = searches(self.rows,country)
        row_of_country = search.linear_search()
        
        #this section uses the found country and then gets all the relevant data about the country
        self.population_density_of_country = self.rows[[1][row_of_country]]
        self.population_of_country = self.rows[[2][row_of_country]]
        self.area_of_country = self.rows[[3][row_of_country]]
        
    def population_effected(self):
        #this calculates the poulation effected by timing the population density and the area effected. this value is then truncated
        population_effected = self.area_effected*self.population_density_of_country
        math.trunc(population_effected)
        if self.area_effected >=self.area_of_country or population_effected >= self.population_of_country:
            population_effected = self.population_of_country
        self.causlty_count_label.config(text= "The casulty count was ~"+population_effected)
        

class searches():
    def __init__(self,rows,country):
        self.array_rows = rows
        self.target = country

    def linear_search(self):
        for x in range (len(self.rows)):
            if self.array_rows[[0][x]] == self.target:
                return x   
            
                
                
            

if __name__ == "__main__":
    app = App()
    app.mainloop()
