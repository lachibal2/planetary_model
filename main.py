from turtle import *
from tkinter import *
import math
import argparse

#calls global variable isRunning to continue drawing
global isRunning
isRunning = True

p = argparse.ArgumentParser()
p.add_argument('-s', '--show', help="shows variable information", required=False, type=str, default='False')
args = p.parse_args()
show = args.show

if show.lower() == 'false':
    show = False

elif show.lower() == 'true':
    show = True

else:
    raise ValueError("-s must be of type boolean")

MAX = 100
MIN = 1
ADD_TO_DISTANCE = 60

if show:
    print("local MAX values: {}, local MIN values: {}".format(MAX, MIN))

def get_fg(distance, mass_planet, mass_sun, grav_const=''):
    #wrapper for force of gravity
    if grav_const == '':
        grav_const = (6.67408) #really is 6.67408 x 10 ** -11

    force_g = (grav_const * mass_planet * mass_sun) / (distance ** 2)
    
    return force_g

def get_cent_accel(force_g, mass):
    return force_g / mass  #based on Newton's 2nd Law (F = m * a)

def scale_accel(acceleration):
    """
    scales acceleration from 1 to 10 for turtle speed
    actual value bounds for MAX=100 and MIN=1:
    upper bound:  0.00026070625
    lower bound:  0.17936253695243212
    """
    lower_bound = get_cent_accel(get_fg(MAX + ADD_TO_DISTANCE, MIN, MIN), MIN)
    upper_bound = get_cent_accel(get_fg(MIN + ADD_TO_DISTANCE, MAX, MAX), MAX)

    if show:
        print("lower_bound: {} \nupper_bound: {}".format(lower_bound, upper_bound))

    width = upper_bound - lower_bound
    scale_factor = 9 / width #9 is the width of the turtle range

    scaled_accel = (scale_factor * acceleration) + 1

    return scaled_accel

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master
        self.start()

    def quit_function(self):
        global isRunning
        isRunning = False
        quit()

    def submit_enteries(self, mass_planet_input, mass_sun_input, distance_input, sub_button, space):
        mass_planet = mass_planet_input.get()
        mass_sun = mass_sun_input.get()
        distance = distance_input.get() + ADD_TO_DISTANCE
        
        if show:
            print("distance: {}\nmass_sun: {}\nmass_planet: {}".format(distance, mass_sun, mass_planet))

        fug = get_fg(distance, mass_planet, mass_sun)
        accel_cent = get_cent_accel(fug, mass_planet)
        scaled_accel = scale_accel(accel_cent)

        sub_button.configure(state=DISABLED)

        if show:
            print('-'*15)
            print("cent_accel: {}".format(accel_cent))
            print("scaled_accel: {}".format(scaled_accel))
            print('-'*15)

        sub_button.configure(state="normal")

        space.delete('all')

        t = RawTurtle(space)
        t.shape('circle')
        t.speed(0)

        if mass_sun < 5:
            half_mass = mass_sun * 2

        else:
            half_mass = mass_sun / 2

        space.create_oval(-1 * half_mass, half_mass, half_mass, -1 * half_mass, fill='yellow')
        
        t.color('blue')

        t.penup()
        t.goto(0, -1 * distance)
        t.pendown()

        t.speed(scaled_accel)
        if math.log10(mass_planet) < 1:
            t_size = math.log10(mass_planet) + 1
        else:
            t_size = math.log10(mass_planet) 

        t.turtlesize(t_size)


        global isRunning
        try:
            while isRunning:
                t.circle(distance)

        except Exception as e:
            print(e)
        

    def start(self):
        master = self.master
        
        exit_button = Button(master, bg='red', text='Exit To Desktop',command=lambda:self.quit_function())
        exit_button.grid(row=5, column=1)

        mass_planet_label = Label(master, text='Mass of planet')
        mass_planet_label.grid(row=0, column=0)

        mass_planet = Scale(master, from_=MIN, to=MAX, orient=HORIZONTAL)
        mass_planet.grid(row=0, column=1)

        mass_sun_label = Label(master, text='Mass of Sun')
        mass_sun_label.grid(row=2, column=0)

        mass_sun = Scale(master, from_=MIN, to=MAX, orient=HORIZONTAL)
        mass_sun.grid(row=2, column=1)

        distance_label = Label(master, text='Distance')
        distance_label.grid(row=1,column=0)

        distance = Scale(master, from_=1, to=MAX, orient=HORIZONTAL)
        distance.grid(row=1, column=1)

        canvas = Canvas(self.master, width=400, height=400, bg='white')
        canvas.grid(row=4)

        submit = Button(text='Model Planet Orbit!', bg='white', bd=5, command=lambda: self.submit_enteries(mass_planet, mass_sun, distance, submit, canvas))
        submit.grid(row=1, column=4)


size = '800x600'

try:
    root = Tk()
    root.geometry(size)
    win = Window(root)
    root.mainloop()

    status = "OK"

except Exception as e:
    status = "fatal, " + str(e)

finally:
    try:
        print("status: {}".format(status))

    except NameError:
        status = "OK"
        print("status: {}".format(status))
