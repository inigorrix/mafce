import json
import importlib
import concurrent.futures
import numpy as np

import pickle
import os
from hx711 import HX711

from PyQt5 import QtCore
from style_sheet_data import style_sheets

import hw_functions
# hay que importarlo primero por separado para poder recargarlo si se calibra la célula de carga
from hw_functions import hx_weight, turn_increment, sim_weight, sim_weight_k, aprox_k

###########
#from random import randint
from time import sleep

##def hx_weight():
##    return randint(-500, 2500)
###########



with open('data.json', 'r') as f:
    values = json.load(f)
data = values['current_values']
defaults = values['default_values']


def set_values(ui, x=1):
    for key in ui.ui_data.keys():
        if x==1:
            ui.ui_data[key] = data[key]
        elif x==0:
            ui.ui_data[key] = defaults[key]


def close(ui):
    ui.sim_w_on = False
    ui.mot_turning, ui.mot_auto_fwd, ui.mot_auto_bwd = False, False, False
    ui.scale_on = False
            

#redondea un número n al múltiplo de p más cercano
def round_int(n, p):
    return round(n/p)*p
    

def tab_change(ui):
    ui.tabWidget.setStyleSheet(style_sheets['tab_widget'])

    ui.sim_w_on = False
    ui.mot_turning, ui.mot_auto_fwd, ui.mot_auto_bwd = False, False, False
    ui.scale_on = False

    if ui.tabWidget.currentIndex()==0:
        reset_sim_tab(ui)
    elif ui.tabWidget.currentIndex()==1:
        reset_motor_tab(ui)
    elif ui.tabWidget.currentIndex()==2:
        scale_tab_scale(ui)        


## TAB SIM WEIGHT FUNCTIONS ##

def reset_sim_tab(ui):
    ui.slider_sim_w.setValue(ui.goal_w)
    ui.start_button.setStyleSheet(style_sheets['start_button'])
    ui.start_button.setText('INICIAR')
    ui.slider_real_w.setStyleSheet('QSlider::groove{background:grey}')
    ui.slider_real_w.setValue(0)
    ui.lcd_real_w.display('----')
    ui.lcd_err_act.display('-----')
    ui.lcd_err_adm.display(ui.ui_data['error'])
    ui.frame_err.setStyleSheet(style_sheets['frame_err'])
    

def slider_sim_w(ui):
    ui.goal_w = round_int(ui.slider_sim_w.value(), ui.ui_data['sim_slider_precision'])
    ui.lcd_sim_w.display(ui.goal_w)


def addsub_w(ui, n):
    ui.goal_w += n
    if ui.goal_w<0:
        ui.goal_w=0
    elif ui.goal_w>2000:
        ui.goal_w=2000
    
    ui.slider_sim_w.setValue(ui.goal_w)
    ui.lcd_sim_w.display(ui.goal_w)


def sim_num_input(ui, n=10):
    text = ui.label_sim_input.text()
    if n<10:
        n_text = text+str(n)
        if int(n_text)>0 and int(n_text)<=2000:
            ui.label_sim_input.setText(n_text)
    elif n==11:
        ui.label_sim_input.setText(text[:-1])
    elif n==12 and len(text)>0:
        ui.goal_w = int(text)
        ui.slider_sim_w.setValue(ui.goal_w)
        ui.lcd_sim_w.display(ui.goal_w)
        ui.label_sim_input.setText('')


def sim_w_loop(ui):
    ui.slider_sim_w.setValue(ui.goal_w)
    
    ui.sim_w_on = not ui.sim_w_on

    if ui.sim_w_on:
        ui.start_button.setStyleSheet(style_sheets['stop_button'])
        ui.start_button.setText('PARAR')

        error, cel_w = ui.ui_data['error'], ui.ui_data['w_cel_carga']
        hxc_w = hx_weight()+cel_w
        n_base, n_pow = 3, 5 
        inc = n_base**n_pow
        dif = ui.goal_w - hxc_w
        k = ui.ui_data['k']

        while ui.sim_w_on:
##            inc, dif, in_err = sim_weight(ui.goal_w, inc, dif, error, n_base, cel_w)
##            real_w = round(ui.goal_w-dif)
            hxc_w, k = sim_weight_k(ui.goal_w, hxc_w, error, k, cel_w)
            real_w = round(hxc_w)
            
            ui.lcd_real_w.display(real_w)
            ui.slider_real_w.setValue(real_w)
            ui.lcd_err_act.display(real_w-ui.goal_w)

            if abs(real_w-ui.goal_w)<ui.ui_data['error']:
                ui.slider_real_w.setStyleSheet('QSlider::groove{background:limegreen}')
                ui.frame_err.setStyleSheet(style_sheets['frame_err_green'])
            elif real_w<0 or real_w>2000:
                ui.slider_real_w.setStyleSheet('QSlider::groove{background:firebrick}')
                ui.frame_err.setStyleSheet(style_sheets['frame_err'])
            else:
                ui.slider_real_w.setStyleSheet('QSlider::groove{background:gold}')
                ui.frame_err.setStyleSheet(style_sheets['frame_err'])

            QtCore.QCoreApplication.processEvents()

    else:
        reset_sim_tab(ui)

        
## TAB MOTOR FUNCTIONS ##

def reset_motor_tab(ui):
    ui.mot_turning = False
    ui.mot_auto_fwd, ui.mot_auto_bwd = False, False
    motor_vel(ui)
    ui.lcd_mot_w.display('----')
    ui.b_enr_auto.setStyleSheet('QPushButton{background:darkslategrey}')
    ui.b_enr_auto.setText('ENROLLAR\nautomáticamente')
    ui.b_des_auto.setStyleSheet('QPushButton{background:darkslategrey}')
    ui.b_des_auto.setText('DESENROLLAR\nautomáticamente')

def motor_vel(ui):
    ui.slider_mot_vel.setMaximum(ui.ui_data['mot_slider_divs']-1)
    p = ui.slider_mot_vel.value()/(ui.ui_data['mot_slider_divs']-1)
    d = ui.ui_data['max_mot_vel']-ui.ui_data['min_mot_vel']
    v = ui.ui_data['min_mot_vel'] + p*d
    
    ui.mot_vel = v/60
    vm, vs = str(round(v, 2)), str(round(ui.mot_vel, 3))
    vmf = vm + '0'*(2-len(vm.split('.')[1]))
    vsf = vs + '0'*(3-len(vs.split('.')[1]))
    vel_text = 'Velocidad\n' + vmf + ' rpm = ' + vsf + ' rps'

    ui.label_mot_vel.setText(vel_text)


def mot_hold_turn(ui, fwd_dir):
    reset_motor_tab(ui)
    ui.mot_turning = True
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(hx_wait, ui)
        while ui.mot_turning:
            turn_increment(1, fwd=fwd_dir, vel=1/ui.mot_vel)
            QtCore.QCoreApplication.processEvents()
    
def mot_stop(ui):
    ui.mot_turning = False

def mot_auto_turn(ui, fwd_dir):
    ui.mot_turning = False
    button_on, button_off = None, None
    des = ''

    if fwd_dir:
        if ui.mot_auto_fwd:
            ui.mot_auto_fwd = False
            button_off = ui.b_enr_auto
        else:
            ui.mot_auto_bwd = False
            ui.mot_auto_fwd = True
            button_on, button_off = ui.b_enr_auto, ui.b_des_auto
    else:
        if ui.mot_auto_bwd:
            ui.mot_auto_bwd = False
            button_off = ui.b_des_auto
        else:
            ui.mot_auto_fwd = False
            ui.mot_auto_bwd = True
            button_on, button_off = ui.b_des_auto, ui.b_enr_auto

    button_off.setStyleSheet('QPushButton{background:darkslategrey}')
    if button_off==ui.b_des_auto: des = 'DES'
    button_off.setText(des+'ENROLLAR\nautomáticamente')
    if button_on != None:
        button_on.setStyleSheet('QPushButton{background:firebrick}')
        button_on.setText('PARAR')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        hx_w = executor.submit(hx_wait, ui)
        while ui.mot_auto_fwd or ui.mot_auto_bwd:
            turn_increment(1, fwd=fwd_dir, vel=1/ui.mot_vel)
            QtCore.QCoreApplication.processEvents()


def hx_wait(ui, x=0, t=.2):
    while ui.mot_turning or ui.mot_auto_fwd or ui.mot_auto_bwd:
        sleep(t)
        ui.lcd_mot_w.display(round(hx_weight())+ui.ui_data['w_cel_carga'])

    
    

## TAB SCALE FUNCTIONS ##
    

def scale_tab_scale(ui):
    ui.scale_on = True
    ui.lcd_sca_cel_w.display(ui.ui_data['w_cel_carga'])
    ui.label_sca_inst.setText("")
    i, n = 0, ui.ui_data['sca_n_measures']
    measurements = np.zeros(n)
    while ui.scale_on:
        measurements[i] = hx_weight()+ui.ui_data['w_cel_carga']
        i+=1
        i = i%n
        if i==0:
            m = round(measurements.mean())
            ui.lcd_sca_w.display(m)
            ui.lcd_sca_colg_w.display(m-ui.ui_data['w_cel_carga'])
            
        QtCore.QCoreApplication.processEvents()


def cambiar_w_celula(ui):
    i = list(ui.ui_data.keys()).index('w_cel_carga')
    button = ui.set_buttons[i]
    button.setChecked(True)
    ui.selected_setting = i
    ui.set_scrollArea.ensureWidgetVisible(button)
    ui.tabWidget.setCurrentIndex(3)
    

def sca_num_input(ui, n=10):
    text = ui.label_sca_input.text()
    if n<10:
        n_text = text+str(n)
        if int(n_text)>0 and int(n_text)<=100000:
            ui.label_sca_input.setText(n_text)
    elif n==11:
        ui.label_sca_input.setText(text[:-1])
    elif n==12 and len(text)>0:
        ui.label_sca_input.setText('')
        if ui.calibration_step==3:
            ui.calibration_step=4
            ui.calibration_info['value']=int(text)
            inst = 'Peso colgado: ' + text + ' g.\n'
            inst2 = 'Pulse Aceptar para guardar la calibración.'
            ui.label_sca_inst.setText(inst+inst2)            


def calibrar_cel(ui, cal_step):
    if cal_step==-1 or cal_step==0:
        ui.calibration_step=-1
        scale_tab_scale(ui)
    elif cal_step==1:
        ui.calibration_step=1
        ui.scale_on = False
        ui.lcd_sca_w.display('----')
        ui.lcd_sca_colg_w.display('----')
        inst = 'Retire el peso de la célula de carga\ny pulse Aceptar.'
        ui.label_sca_inst.setText(inst)
        ui.calibration_info['hx'] = HX711(dout_pin=21, pd_sck_pin=20)
    elif cal_step==2:
        ui.calibration_step=2
        ui.calibration_info['hx'].zero()
        inst = 'Cuelgue un peso conocido en la célula\n'
        inst2 = 'de carga y pulse Aceptar.'
        ui.label_sca_inst.setText(inst+inst2)
    elif cal_step==3:
        ui.calibration_step=3
        ui.calibration_info['reading'] = ui.calibration_info['hx'].get_data_mean()
        inst = 'Introduzca el peso colgado (en gramos)\ny pulse Enter.'
        ui.label_sca_inst.setText(inst)
    elif cal_step==5:
        ui.calibration_step=5
        ratio = ui.calibration_info['reading']/ui.calibration_info['value']
        ui.calibration_info['hx'].set_scale_ratio(ratio)
        with open('new_swap_file.swp', 'wb') as swap_file:
            pickle.dump(ui.calibration_info['hx'], swap_file)
            swap_file.flush()
            os.fsync(swap_file.fileno())
        os.replace('new_swap_file.swp', 'swap_file.swp')
        inst = 'Calibración guardada correctamente.\nPulse Aceptar.'
        ui.label_sca_inst.setText(inst)
    if cal_step==6:
        ui.calibration_step=-1
        importlib.reload(hw_functions)
        scale_tab_scale(ui)

        

def estimar_k(ui):
    ui.label_sca_inst.setText('Calculando k...')
    QtCore.QCoreApplication.processEvents()
    aprox_k(ui, show_ui=True)


## TAB SETTINGS FUNCTIONS ##

settings_options=[
    'Rigidez K del sistema',
    'Precisión del controlador deslizante del simulador\nde peso',
    'Error admisible en la simulación de peso (g)',
    'Velocidad mínima para la pestaña Motor (rpm)',
    'Velocidad máxima para la pestaña Motor (rpm)',
    'Número de divisiones del controlador deslizante\nde la pestaña Motor',
    'Peso de la célula de carga (g)',
    'Número de medidas con las que se hace la media\nen la pestaña Báscula',
    ]

def settings_text(ui):
    ui_values = list(ui.ui_data.values())
    saved_values = list(data.values())
    default_values = list(defaults.values())

    for i, text in enumerate(settings_options):
        a = '\nValor actual: ' + str(ui_values[i])
        g = '\nValor guardado: ' + str(saved_values[i])
        d = '\nValor por defecto: ' + str(default_values[i])
        ui.set_buttons[i].setText(text + d + g + a)
    

def set_num_input(ui, n=10):
    text = ui.label_set_input.text()
    if n<10:
        n_text = text+str(n)
        if int(n_text)>0 and int(n_text)<=999999:
            ui.label_set_input.setText(n_text)
    elif n==11:
        ui.label_set_input.setText(text[:-1])
    elif n==12 and len(text)>0 and ui.selected_setting!=None:
        set_property = list(data.keys())[ui.selected_setting]
        ui.ui_data[set_property] = int(text)

        ui.label_set_input.setText('')
        settings_text(ui)


def select_setting(ui, button_n):
    if button_n == ui.selected_setting:
        ui.set_buttons[button_n].setAutoExclusive(False)
        ui.set_buttons[button_n].setChecked(False)
        ui.set_buttons[button_n].setAutoExclusive(True)
        ui.selected_setting = None
    else:
        ui.selected_setting = button_n


def settings_menu(ui, option):
    if option==1:
        for key in ui.ui_data.keys():
            data[key]=ui.ui_data[key]

        new_values = {'default_values':defaults, 'current_values':data}
        with open('data.json', 'w') as f:
            json.dump(new_values, f, indent=4)

        settings_text(ui)
        
    elif option==2:
        ui.tabWidget.setCurrentIndex(0)
        
    elif option==3:
        set_values(ui, 0)
        settings_text(ui)
        
    elif option==4:
        set_values(ui)
        settings_text(ui)
    

