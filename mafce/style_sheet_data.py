#Style Sheets

##############################

tab_widget_stsh = ('''
QTabWidget::tab-bar{
    alignment: center;
}

QTabWidget::pane{
    border: 0px solid grey;
}

QTabBar::tab:selected{
    padding: 5px;
    padding-top: 15px;
    padding-bottom: 15px;
    border-radius: 7px;
    margin: -2px;
    margin-right: -6px;
    border: 4px solid grey;
}

QTabBar::tab:!selected{
    background-color: silver;
    padding: 7px;
    border-radius: 7px;
    margin: -2px;
    border: 4px solid grey;
}

QWidget{
    background-color: gainsboro;
}

QPushButton{
    font: bold 15px;
    background-color: silver;
    border-radius: 10px;
    border: 2px solid black;
}

QPushButton:pressed{
    background-color: darkgrey;
}

QSlider::handle:vertical{
    margin: -15px;
    height: 40px;
    border-radius: 20px;
    background: black;
}
QSlider::groove:vertical{
    border:2px solid black;
    margin: 20px;
    border-radius: 5px;
    width: 10px;
    background: darkslategray;
}

QSlider::handle:horizontal{
    margin: -15px;
    width: 40px;
    border-radius: 20px;
    background: black;
}
QSlider::groove:horizontal{
    border:2px solid black;
    margin: 20px;
    border-radius: 5px;
    height: 10px;
    background: darkslategray;
}

QLCDNumber{
    border: 0px;
}
''')

##############################

scroll_bar_stsh = ('''
QScrollArea{
    border:1px solid gray;
    border-radius: 2px;
}

QScrollBar{
    width: 30px;
}

QScrollBar::add-line, QScrollBar::sub-line{
    border: 2px solid black;
    background: darkgray;
    border-radius: 10px;
}

QScrollBar::handle{
    background-color: darkgray;
    border: 2px solid black;
    border-radius: 10px;
    margin-top: 30px;
    margin-bottom: 30px;
}

QScrollBar::up-arrow, QScrollBar::down-arrow {
    width: 10px;
    height: 10px;
    border-radius: 5px;
    background-color: black;
}


QRadioButton::indicator{
    width: 10px;
}
QRadioButton{
    background-color: darkgray;
    border-radius: 10px;
    padding: 5px;
    padding-left: 10px;
    padding-right: 10px;
}
QRadioButton::checked{
    border: 2px solid black;
    border-radius: 10px;
}
''')

##############################

start_button_stsh = ('''
QPushButton{
    font: bold 30px;
    height: 160px;
    width: 160px;
    border-radius: 80px;
    color: white;
    background-color: forestgreen;
}
QPushButton::pressed{
    background-color: green;
}
''')

##############################

stop_button_stsh = ('''
QPushButton{
    font: bold 30px;
    height: 160px;
    width: 160px;
    border-radius: 80px;
    color: white;
    background-color: firebrick;
}
QPushButton::pressed{
    background-color: darkred;
}
''')

##############################

frame_mot_stsh = ('''
QFrame{
    border: 0px;
}

QPushButton{
    height: 160px;
    border-radius: 70px;
    color: white;
    background-color: darkslategray;
}
QPushButton::pressed{
    background-color: #1e3333;
}
''')

##############################

frame_err_stsh = ('''
QFrame{
    border: 2px solid black;
    border-radius: 25px;
    color: black;
    background-color: gold;
}

QLabel, QLCDNumber{
    border: 0px;
}
''')

##############################

frame_err_green_stsh = ('''
QFrame{
    border: 2px solid black;
    border-radius: 25px;
    color: black;
    background-color: limegreen;
}

QLabel, QLCDNumber{
    border: 0px;
}
''')

##############################

frame_sca_cel_w_stsh = ('''
QFrame{
    border: 2px solid black;
    border-radius: 10px;
    background-color: white;
    color: black;
}

QLabel, QLCDNumber{
    border: 0px;
}
''')

##############################

frame_blue_buttons_stsh = ('''
QFrame{
    border: 0px;
}

QPushButton{
    padding: 5px;
    border-radius: 40px;
    color: white;
    background-color: darkslategray;
}
QPushButton::pressed{
    background-color: #1e3333;
}
''')

##############################

green_button_stsh = ('''
QPushButton{
    color: white;
    background-color: forestgreen;
}
QPushButton::pressed{
    background-color: darkgreen;
}
''')

##############################

red_button_stsh = ('''
QPushButton{
    color: white;
    background-color: firebrick;
}
QPushButton::pressed{
    background-color: darkred;
}
''')

##############################

yellow_button_stsh = ('''
QPushButton{
    color: white;
    background-color: goldenrod;
}
QPushButton::pressed{
    background-color: peru;
}
''')

##############################

label_sca_inst_stsh = ('''
QLabel{
    border: 4px solid slategray;
    border-radius: 10px;
    font: bold;
    color: white;
    background: black;
}
''')

##############################

label_num_input_stsh = ('''
QLabel{
    border: 2px solid black;
    border-radius: 10px;
    font: bold 15px;
    color: black;
    background: white;
}
''')

##############################
##############################
##############################

style_sheets = {
    'tab_widget': tab_widget_stsh,
    'scroll_bar': scroll_bar_stsh,
    'frame_err': frame_err_stsh,
    'frame_err_green': frame_err_green_stsh,
    'start_button': start_button_stsh,
    'stop_button': stop_button_stsh,
    'frame_mot': frame_mot_stsh,
    'frame_sca_cel_w': frame_sca_cel_w_stsh,
    'frame_blue_buttons': frame_blue_buttons_stsh,
    'green_button': green_button_stsh,
    'red_button': red_button_stsh,
    'yellow_button': yellow_button_stsh,
    'label_sca_inst': label_sca_inst_stsh,
    'label_num_input': label_num_input_stsh,
    }
