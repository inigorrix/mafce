import pickle, os
import concurrent.futures
from hx711 import HX711
import RPi.GPIO as GPIO
import numpy as np
from time import sleep


def turn(n, delay):
    for i in range(n):
        GPIO.output(pstep, True)
        sleep(delay)
        GPIO.output(pstep, False)
        sleep(delay)


def turn_angle(angle, fwd=True, vel=1):
    GPIO.output(pdir, fwd)
    n = round(step_count * angle/360)
    delay = vel / (2*step_count)
    turn(n, delay)


def turn_increment(n, fwd=True, vel=1):
    GPIO.output(pdir, int(fwd))
    delay = vel / (2*step_count)
    turn(n, delay)

def hx_no_false():
    hx_m = hx.get_weight_mean(1)
    if not(hx_m) or abs(hx_m)>9999:
        hx_m = hx_no_false()
    return hx_m

def hx_weight(x = 0, ei = 4):
    if x == 0:
        ws = np.array(hx_no_false())
        run = True
        while run:
            ws = np.append(ws, hx_no_false())
            ws.sort()
            l_ws = len(ws)-1
            for i in range(l_ws):
                e_ws = ws[i+1]-ws[i]
                if e_ws<ei**l_ws:
                    if l_ws>4:
                        hx_w = ws.mean()
                    else:
                        hx_w = (ws[i+1]+ws[i])/2
                    run=False
                    break
                
    else: hx_w = hx.get_weight_mean(x)

    return hx_w


def aprox_k(ui=None, show_ui=False):
    global k
    n0 = 3**4
    turn_angle(90, False)
    turn_angle(90, True)
    hx_w = hx_weight()
    interv = (100, 200)
    midpoint = (interv[0]+interv[1])/2
    fwd = hx_w<midpoint
    while (hx_w<interv[0]) or (hx_w>interv[1]):
        prev_fwd = fwd
        fwd = hx_w<midpoint
        if fwd!=prev_fwd and n0>1:
            n0 = round(n0/3)
        turn_increment(n0, fwd)
        hx_w = hx_weight()
    
    points, n1, w_max = 5, 5, 1750
    sleep(.25)
    w0 = hx_weight()
    turn_increment(n1, True)
    sleep(.25)
    w1 = hx_weight()
    print(w0, w1)
    k_arr = np.array((w1-w0)/n1)
    print(k_arr*step_count/360)
    for i in range(points*2):
        fwd = i<points
        k_m = k_arr.mean()
        pts_left = points-i%points
        f_tot = w_max-w1 if fwd else w1-midpoint
        n2 = round(f_tot / (k_m*pts_left))

        for j in range(3):
            fwd_dir = fwd
            if j%2:
                fwd_dir = not(fwd_dir)
            turn_increment(n2, fwd_dir)
            w0 = w1
            w1 = hx_weight()
            k_arr = np.append(k_arr, (abs(w1-w0)/n2))

            kd_i, kd_m = k_arr[-1]*step_count/360, k_arr.mean()*step_count/360
            print(w1, kd_i, kd_m)
            
    k_deg_arr = k_arr*step_count/360
    k_min, k_max = round(k_deg_arr.min(), 2), round(k_deg_arr.max(), 2)
    print(k_deg_arr)
    print(k_min, k_max)
    k = k_deg_arr.mean()
    print('\nk = ' + str(round(k, 3)) + ' g/º')
    if show_ui:
        k_minmax = 'kmin, kmax:  '+str(k_min)+' - '+str(k_max)
        k_med_minmax = '\nMedia kmin-kmax:  '+str(round((k_min+k_max)/2, 3))
        k_med = '\n\nk media de las '+str(len(k_arr))+' medidas:  '+str(round(k, 2))+' g/º'
        k_text = k_minmax + k_med_minmax + k_med
        ui.label_sca_inst.setText(k_text)


def aprox_k1():
    global k
    hx_w, n0 = hx_weight(), 3**5
    interv = (50, 150)
    midpoint = (interv[0]+interv[1])/2
    fwd = hx_w<midpoint
    while (hx_w<interv[0]) or (hx_w>interv[1]):
        prev_fwd = fwd
        fwd = hx_w<midpoint
        if fwd!=prev_fwd and n0>1:
            n0 = round(n0/3)
        turn_increment(n0, fwd)
        hx_w = hx_weight()
    
    points, n1, w_max = 5, 80, 1750
    w0 = hx_weight()
    turn_increment(n1, True)
##    sleep(.4)
    w1 = hx_weight()
    print(w0, w1)
    k_arr = np.array((w1-w0)/n1)
    print(k_arr*step_count/360)
    for i in range(points*2):
        fwd = i<points
        k_m = k_arr.mean()
        pts_left = points-i%points
        f_tot = w_max-w1 if fwd else w1-midpoint
        n2 = round(f_tot / (k_m*pts_left))
        turn_increment(n2, fwd)
        
##        sleep(.4)
        w0 = w1
        w1 = hx_weight()
        if not(fwd): n2 *= -1
        k_arr = np.append(k_arr, ((w1-w0)/n2))
        print(w1, k_arr[-1]*step_count/360)
            
    print(k_arr*step_count/360)
    k = k_arr.mean()
    print('\nk = ' + str(round(k*step_count/360, 3)) + ' g/º')


def sim_weight_k_loop(weight, error=5, k=6):
    hx_w = hx_weight()
    while True:
        hx_w, k = sim_weight_k(weight, hx_w, error, k)

def sim_weight_k(weight, hx_w, error=5, k=6, cel_w=0):
    inc_k = k*360/step_count
    dif = weight-hx_w
    
    if abs(dif)>(error/2)**.5:
        fwd = dif>0
        inc = round(abs(dif)/inc_k)
        if inc==0:
            inc = 1 
        turn_increment(inc, fwd)
        if abs(dif)>error:
            print(hx_w, inc, round(inc_k*step_count/360, 3))
        else:
            print(round(hx_w, 2),'\t\t\t', round(dif, 2), inc)
        sleep(.05)
        
        new_hx_w = hx_weight()+cel_w
        inc_k = (abs(new_hx_w-hx_w)/inc + inc_k)/2
        if inc_k*step_count/360>500:
            inc_k = 500*360/step_count
        elif inc_k*step_count/360<1:
            inc_k = 1*360/step_count
        
        hx_w = new_hx_w
        
    else:
        print(round(hx_w, 2),'\t\t\t', round(dif, 2))
        sleep(.01)
        hx_w = hx_weight()+cel_w

    return hx_w, inc_k*step_count/360
            


def sim_weight_loop(weight, error=5, n_base=3, n_pow=5):
    inc = n_base**n_pow
    dif = weight-hx_weight()
    while True:
        inc, dif, in_err = sim_weight(weight, inc, dif, error, n_base)

def sim_weight(weight, inc, dif, error=5, n_base=3, cel_w=0):
    hx_w = hx_weight()+cel_w
    prev_dif = dif
    dif = weight-hx_w
    in_err = False
    
    if abs(dif)>(error/2)**.5:
        in_err = False
        print(round(hx_w), '\t\t\t\t', round(dif, 1))
        fwd = dif>0
        if (dif*prev_dif)<0 and inc>1: inc = round(inc/n_base)
        turn_increment(inc, fwd)
        sleep(.05)
    else:
        in_err = True
        print(round(hx_w, 2),'\t', round(dif, 2))
        sleep(.1)

    return inc, dif, in_err


def change_resolution(new_res):
    global step_count
    if new_res in resolutions:
        GPIO.output(mode, resolutions[new_res])
        step_count = 200*new_res
    else: print('Resolution can be: 1, 2, 4, 8, 16\n')


#get data from a test run
#turn_type [i]ncrement / [a]ngle
def get_data(n, goal=2000, turn_type='a', sleep_t = 0) :
    if turn_type == 'i':
        inc = round(n)
        angle = inc * 360/step_count
    elif turn_type == 'a':
        ang = n
        inc = round(step_count * ang/360)
        angle = inc * 360/step_count
    print('Turn angle: ', angle, '\tIncrement: ', inc, '\n')
    
    total_angle, hx_w = 0, hx_weight(7)
    data = [(total_angle, hx_w)]
    fwd = hx_w < goal
    while (hx_w<goal)==fwd:
        turn_increment(inc, fwd)
        sleep(sleep_t)
        hx_w = hx_weight(7)
        total_angle += angle
        data.append((total_angle, hx_w))
        print(data[-1], '\t\t', data[-1][1]-data[-2][1])
    print('\n', data)
    
    save = input('\nSave data? Y/n: ')
    if save.lower()=='y' or save=='':
        data_name = input('Data name: ').replace(' ', '')
        info = data_name + ' = ' + str(data) + '\n\n'
        with open('data.py', 'a') as data_file:
            data_file.write(info)



def clean():
    GPIO.cleanup()


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


hx = HX711(dout_pin=21, pd_sck_pin=20)
swap_file_name = 'swap_file.swp'

if os.path.isfile(swap_file_name):
    with open(swap_file_name, 'rb') as swap_file:
        hx = pickle.load(swap_file)


pdir, pstep = 24, 23
ms1, ms2, ms3 = 14, 15, 18

pins = (pdir, pstep, ms1, ms2, ms3)
mode = (ms1, ms2, ms3)
resolutions = { 1: (False, False, False),
                2: (True, False, False),
                4: (False, True, False),
                8: (True, True, False),
               16: (True, True, True) }

step_count = 200

GPIO.setup(pins, GPIO.OUT)
change_resolution(16)




