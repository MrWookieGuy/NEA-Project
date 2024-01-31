#this imports the relevant libraries to the program.
from asyncio.windows_events import NULL
from tkinter import messagebox, ttk
import tkinter
import tkintermapview
import math
import csv
from googletrans import Translator

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
location_options = NULL
nuclear_options = NULL


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        
        #geting relevant global variables
        global location_options
        global nuclear_options

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
        self.explosive_value_submit_button = tkinter.Button(self, text="Detonate", command = lambda:validation.validate(self.explosive_value_submittion))
        self.explosive_value_submit_button.grid(row=2, column = 0)
        
        #this is setting up the initial values for the map in this program.
        global the_map 
        the_map = tkintermapview.TkinterMapView(self, width=int(screensizex)*3/4, height=int(screensizey)*8/10, corner_radius=0)
        the_map.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        the_map.set_position(51.51279, -0.09184)
        the_map.set_zoom(12)

        #this it to create a map marker, which will bbe used as the position of the nukes that are placed.
        def add_marker_event(coords):
            global marker_placed
            global the_map
            if marker_placed == False:    
                self.new_marker = the_map.set_marker(coords[0], coords[1], text = "Nuke")
                global centre_coords
                centre_coords = coords
                marker_placed = True

        #this is the set up for the dropdown for nuclear value presets      
        def display_nuclear_selection():
            selection = nuclear_options.get()
            messagebox.showinfo(message=f"The selected value is: {selection}",title="Selection")
               
        nuclear_options = ttk.Combobox(
            state="readonly",
            values= [
            "Custom amount",
            "Davy Crockett - smallest US bomb produced(20t)",
            "Little Boy - Hiroshima  Bomb(15kt)",
            "Gadget - Trinity test(20kt)",
            "Fat Man - Nagasaki bomb(20kt)",
            "W-76 - common in US & UK SLBM arsenal(100kt)",
            "Ivy King - Largest pure fission weapon tested  by USA(500kt)",
            "Ivy Mike - First H-bomb(10.4Mt)",
            "Castle Bravo - Largest US bomb tested(15Mt)",
            "Tsar Bomba - largest USSR bomb tested(50Mt)",
            "Tsar Bomba - largest USSR bomb designed(100Mt)"]
        )
        nuclear_options.grid(row = 1, column= 4)
        display_selection_nuclear_options = ttk.Button(text="Display selection", command=display_nuclear_selection)
        display_selection_nuclear_options.grid(row = 2, column=4)
        


        #this is the set up for the dropdown for position presets
        def display_location_selection():
            selection = location_options.get()
            messagebox.showinfo(message=f"The selected location is:{selection}", title="Selection")
        
        location_options = ttk.Combobox(
            state="readonly",
            values=[
                "Custom location",
                "Berlin",
                "Nagasaki",
                "Hiroshima",
                "Trinity site",
                "Moscow",
                "NYC",
                "Paris"
                ]
            )
        location_options.grid(row = 1, column= 5)
        display_location_selection_options = ttk.Button(text = "Display selection", command=display_location_selection)    
        display_location_selection_options.grid(row = 2, column= 5)
               

        #this is the code  which creates the help pop-up window,
        def help_popup():
            popup = tkinter.Tk()
            popup.wm_title = ("Help popup")
            help_label_1 = tkinter.Label(popup, text = "To choose the place you wish to detonate the nuke you need to right click on the map,", font = "Helvetica")
            help_label_1.pack(side = "top", fill = "x", pady=10)
            help_label_2 = tkinter.Label(popup, text = "this will bring up a menu where you can either place a nuke, reset the map, or copy the co-ordinates of your click(this is done by clicking on the coordinates that appear)", font = "Helvetica")
            help_label_2.pack(fill = "x", pady=10)
            help_label_3 = tkinter.Label(popup, text = "Once you have put down a marker, you can enter a amount of TNT equivilent for the explosion. and an approximate casulty count, based on the population density of the country you are in.", font = "Helvetica")
            help_label_3.pack(fill = "x", pady=10)
            help_label_4 = tkinter.Label(popup, text = "Then click on detonate, and it will display the area of effect as well as giving the radius of the explosion, ", font = "Helvetica")
            help_label_4.pack(fill = "x", pady=10)
            help_label_5 = tkinter.Label(popup, text = "and an approximate casulty count, based on the population density of the country you are in.", font = "Helvetica")
            help_label_5.pack(fill = "x", pady=10)
            back_button = tkinter.Button(popup, text = "Okay", command = popup.destroy)
            back_button.pack()
            popup.mainloop()


        #this is the method to reset the map, and remove all the markers/paths on i
        def reset_map(self):
            global the_map
            global marker_placed
            global area_of_effect
            if marker_placed == True:
                self.new_marker.delete()
                area_of_effect.delete()
            marker_placed = False
            
        #this is to add the rightclick commands to the program
        the_map.add_right_click_menu_command(label="Place nuke", command=add_marker_event, pass_coords=True)    
        the_map.add_right_click_menu_command(label = "Clear map", command = lambda:reset_map(self))
        
        #setting up the help button
        self.help_button = tkinter.Button(self, text = "Help?", command = lambda:help_popup())  
        self.help_button.grid(row = 0, column=4)

    #this is the section for checking the explosive preset dropdown box and returning whether there is a preset, and the relevant explosive value
def check_if_explosive_preset():
    global nuclear_options
    preset = nuclear_options.get()
    if preset  == "Davy Crockett - smallest US bomb produced(20t)":
        return True, 0.02
    elif preset == "Little Boy - Hiroshima  Bomb":
        return True, 15
    elif preset == "Gadget - Trinity test(20kt)":
        return True, 20
    elif preset == "Fat Man - Nagasaki bomb(20kt)":
        return True, 20
    elif preset == "W-76 - common in US & UK SLBM arsenal(100kt)":
        return True, 100
    elif preset == "Ivy King - Largest pure fission weapon tested  by USA(500kt)":
        return True, 500
    elif preset == "Ivy Mike - First H-bomb(10.4Mt)":
        return True, 10400
    elif preset == "Castle Bravo - Largest US bomb tested(15Mt)":
        return True, 15000
    elif preset == "Tsar Bomba - largest USSR bomb tested(50Mt)":
        return True, 50000
    elif preset == "Tsar Bomba - largest USSR bomb designed(100Mt)":
        return True, 100000
    else:
        return False, NULL

    #this is the section for checking the location preset dropdown box and returning whether there is a preset, and the relevant coordinates
def check_if_location_preset():
    global location_options
    preset = location_options.get()
    if preset == "Berlin":
        return True, [52.51622358232272, 13.377108044505544]
    elif preset == "Trinity site":
        return True, [33.67725713634414, -106.47543730542701]
    elif preset == "Nagasaki":
        return True, [32.75078235183071, 129.8681544511882]
    elif preset == "Hiroshima":
        return True, [34.39643055690335, 132.45248918400182]
    elif preset == "Moscow":
        return True, [55.7540062676168, 37.620150124870854]
    elif preset == "Paris":
        return True, [48.86596449522448, 2.3198210567573696]
    elif preset == "NYC":
        return True, [40.74785480849046, -73.98509623331023]
    else:
        return False, NULL

class validate_data(App):

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
        
        checking_explosive_preset = NULL  
        checking_explosive_preset = check_if_explosive_preset()
        if checking_explosive_preset[0] == True:
            tnt_equivilent = checking_explosive_preset[1]
        print(tnt_equivilent)  
        
        #this is the beginning of the validation of the program, limiting the amount of chrarcters that can be used for the input
        if len(str(tnt_equivilent)) < 20 or checking_explosive_preset[0] == True:
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
                        
                        #this section if defining and then drawing the area of effect onto the map, furthermore it calculaes and outputs the casulty count
                        if marker_placed == True:
                            global centre_coords
                            global the_map
                            

                            checking_location_preset = check_if_explosive_preset()
                            if checking_explosive_preset[0] == True:
                                centre_coords = checking_explosive_preset[1]
                            
                            area_of_effect = draw_area_of_effect(radius_of_the_explosion,centre_coords)
                            area_of_effect.defining_path()
                            area_of_effect.creating_area_of_effect_display(the_map)
                            
                            #this is the section which gets and subsequently displays the casulties
                            casulty_count = casulty_count_calculation_and_display(radius_of_the_explosion)
                            casulty_count.get_country_data()
                            casulty_count.population_effected()
                        

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
                            
                            #this is the section which gets and subsequently displays the casulties
                            casulty_count = casulty_count_calculation_and_display(radius_of_the_explosion)
                            casulty_count.get_country_data()
                            casulty_count.population_effected()
                        
                        
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
        #this defibnes the parameters of the class, these being the array of points around the area of effect, the radius of the explosion, converted into change in decimal coordinates
        self.array_of_points = [[]]
        self.radius_of_the_explosion = int(radius)/111000
        self.coordinates_of_explosion_x = coordinates[1]
        self.coordinates_of_explosion_y = coordinates[0]
       
    def defining_path(self):
        #this section of the code is for setting the points of the circle, and then putting them in an array for the method
        self.array_of_points[0] = [self.coordinates_of_explosion_y+self.radius_of_the_explosion, self.coordinates_of_explosion_x]

        #the comments before each loop shows which quarter of the circle is being defined at each section
        #+X, +Y
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
        #self.array_of_points.append[self.coordinates_of_explosion_y+self.radius_of_the_explosion,self.coordinates_of_explosion_x]
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
        self.area_effected = radius**2*math.pi
        self.row_of_country = NULL
        self.causlty_count_label = tkinter.Label("")
        self.causlty_count_label.grid(row = 0, column = 3)
        
        
    def get_country_data(self):
        #this program gets the country which the arrow is in, it then uses a linear searchto find the country in the csv file. this is done after translating the country to english
        global centre_coords
        country = tkintermapview.convert_coordinates_to_country(centre_coords[0],centre_coords[1])
        print(country)
        #this section translates the text from its native language to english
        translator = Translator()
        country = translator.translate(country)
        #this section is for setting up and handeling the csv file
        searching_for_country = CSV_handling(country.text)
        country_dictionary = searching_for_country.search_for_country()
        
        #this is for setting any relevant data from the country
        self.population_of_country = searching_for_country.get_values(country_dictionary, "Area")
        self.area_of_country = searching_for_country.get_values(country_dictionary, "Population")
        self.population_density_of_country = searching_for_country.get_values(country_dictionary,"population density")
        
    def population_effected(self):
        #this calculates the poulation effected by timing the population density and the area effected. this value is then truncated
        population_effected = (self.area_effected/1000000)*float(self.population_density_of_country[0])
        if self.area_effected >=float(self.area_of_country[0]) or population_effected >= float(self.population_of_country[0]):
            population_effected = self.population_of_country
        self.causlty_count_label.config(text= "The casulty count was ~"+str(math.trunc(population_effected)))
        

class CSV_handling():
    def __init__(self,country):
        #this section is opening, and then copying the data in the csv to a list of dictionaries
        try:
            with open("pop density.csv", "r") as file:
                csv_reader = csv.DictReader(file)
                self.data = list(csv_reader)
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found")
        
        #this is setting the target country for the search
        self.target = country
        
    def search_for_country(self):
        return list(filter(lambda countries: countries["Country (or dependent territory)"] == self.target, self.data))
    

    def get_values(self,lst, key):
        #this gets the values that are in the new filtered list
        if not lst:
             return []
        first_dict = lst[0]
        if key in first_dict:
             result  = [first_dict[key]]
        else:
             result = []
        return result    
            
if __name__ == "__main__":
    app = App()
    app.mainloop()
