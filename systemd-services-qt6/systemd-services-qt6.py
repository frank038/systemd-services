#!/usr/bin/env python3

# version 0.3

USE_STATIC = 1 # 0: do not search for services in static state; 1: does
use_font_size = 0 # 0: use system default font size; any number: use this value
BUTTON_SIZE = 48
dialWidth = 400 # dialog width

from PyQt6.QtCore import (Qt,QObject,QRect,QSize,QMargins)
from PyQt6.QtWidgets import (QFrame,QLayout,QSpacerItem,QScrollArea,QSizePolicy,QBoxLayout,QLabel,QPushButton,QApplication,QDialog,QGridLayout,QMessageBox,QTabWidget,QWidget,QComboBox,QStyle)
from PyQt6.QtGui import (QIcon)

import sys,os
import subprocess

MY_HOME = os.path.expanduser('~')

class firstMessage(QWidget):
    def __init__(self, *args):
        super().__init__()
        title = args[0]
        message = args[1]
        self.setWindowTitle(title)
        # self.setWindowIcon(QIcon("icons/.svg"))
        box = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        box.setContentsMargins(5,5,5,5)
        self.setLayout(box)
        label = QLabel(message)
        box.addWidget(label)
        button = QPushButton("Close")
        box.addWidget(button)
        button.clicked.connect(self.close)
        self.show()


app = None
WINW = 800
WINH = 600

try:
    with open("winsize.cfg", "r") as ifile:
        fcontent = ifile.readline()
    aw, ah = fcontent.split(";")
    WINW = int(aw)
    WINH = int(ah)
except:
    try:
        with open("winsize.cfg", "w") as ifile:
            ifile.write("800;600")
    except:
        fm = firstMessage("Error", "The file winsize.cfg cannot be read/created.")
        sys.exit(app.exec())


##### GET THE LIST OF SERVICES
def on_system_services():
    SYSTEM_SERVICES_TMP = subprocess.check_output(["systemctl", "list-units", "--no-legend", "--no-pager", "--type=service", "--quiet", "--no-block"])
    SYSTEM_SERVICES = SYSTEM_SERVICES_TMP.decode().split("\n")
    ell = []
    # field 0: name - field 1: status - field 2-:description
    system_list = []
    for el in SYSTEM_SERVICES:
        ell.append(el.lstrip(" ").split(" "))

    for el in ell[:]:
        if el == ['']:
            continue
        ell_item = []
        for eel in el:
            if eel != '':
                ell_item.append(eel)
        system_list.append(ell_item)

    del ell
    return system_list

def on_user_services():
    USER_SERVICES_TMP = subprocess.check_output(["systemctl", "list-units", "--no-legend", "--no-pager", "--type=service", "--quiet", "--no-block", "--user"])
    SYSTEM_SERVICES = None
    # field 0: name - field 1: status - field 2-:description
    user_list = []
    if SYSTEM_SERVICES_TMP:
        SYSTEM_SERVICES = SYSTEM_SERVICES_TMP.decode().split("\n")
        ell = []
        for el in ell[:]:
            if el == ['']:
                continue
            ell_item = []
            for eel in el:
                if eel != '':
                    ell_item.append(eel)
            user_list.append(ell_item)
        del ell
        return user_list

##### END LIST OF SERVICES


##### GET THE STATUS OF SERVICES
def on_status_system():
    if USE_STATIC:
        STATUS_SYSTEM_TMP = subprocess.check_output(["systemctl", "--full", "list-unit-files", "--no-legend", "--no-pager", "--type=service", "--quiet", "--no-block", "--state=enabled,disabled,masked,static"])
    else:
        STATUS_SYSTEM_TMP = subprocess.check_output(["systemctl", "--full", "list-unit-files", "--no-legend", "--no-pager", "--type=service", "--quiet", "--no-block", "--state=enabled,disabled,masked"])
    STATUS_SYSTEM = STATUS_SYSTEM_TMP.decode().split("\n")
    # name.service - state - status
    status_system_list = []
    ell = []
    for el in STATUS_SYSTEM:
        ell.append(el.lstrip(" ").split(" "))

    for el in ell:
        if el == ['']:
            continue
        for eel in el[:]:
            if eel == '':
                el.remove(eel)
        status_system_list.append(el)
    
    del ell
    return status_system_list

def on_status_user():
    STATUS_USER_TMP = subprocess.check_output(["systemctl", "--full", "list-unit-files", "--no-legend", "--no-pager", "--type=service", "--quiet", "--no-block", "--user", "--state=enabled,disabled,masked"])
    if STATUS_USER_TMP:
        STATUS_USER = STATUS_USER_TMP.decode().split("\n")
        # name.service - state - status
        status_user_list = []
        ell = []
        for el in STATUS_USER:
            ell.append(el.lstrip(" ").split(" "))

        for el in ell:
            if el == ['']:
                continue
            for eel in el[:]:
                if eel == '':
                    el.remove(eel)
            status_user_list.append(el)
        
        del ell
        return status_user_list

##### END STATUS OF SERVICES



class MainWin(QWidget):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.setWindowTitle("ServicesQt6")
        # self.setWindowIcon(QIcon("icon"))
        self.pixel_ratio = max(1,self.devicePixelRatio())
        self.resize(int(WINW/self.pixel_ratio), int(WINH/self.pixel_ratio))
        # main box
        self.vbox = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.vbox.setContentsMargins(QMargins(2,2,2,2))
        self.setLayout(self.vbox)
        # main tab
        self.gtab = QTabWidget()
        self.gtab.setContentsMargins(2,2,2,2)
        self.gtab.setMovable(False)
        self.gtab.setTabsClosable(False)
        self.vbox.addWidget(self.gtab)
        
        ##### SYSTEM
        _name = "System"
        self.page1 = QWidget()
        
        self.gtab.addTab(self.page1, _name)
        self.pagebox = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.page1.setLayout(self.pagebox)
        
        self.buttonbox = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.pagebox.addLayout(self.buttonbox)
        
        self.reload_btn = QPushButton("reload")
        self.reload_btn.clicked.connect(self.on_reload)
        self.buttonbox.addWidget(self.reload_btn, 0, Qt.AlignmentFlag.AlignTop)
        
        self.quit_btn = QPushButton("exit")
        self.quit_btn.clicked.connect(self.close)
        self.buttonbox.addWidget(self.quit_btn, 0, Qt.AlignmentFlag.AlignTop)
        
        self.scroll_widget = QWidget()
        self.scroll_widget.setContentsMargins(QMargins(0,0,0,0))
        self.scroll_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.scroll_layout = QGridLayout()
        self.scroll_layout.setContentsMargins(QMargins(0,0,0,0))
        self.scroll_layout.setSpacing(0)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_layout.setColumnStretch(3, 10)
        # self.scroll_layout.setContentsMargins(QMargins(10,10,10,10))
        self.scroll_layout.setHorizontalSpacing(10)
        self.scroll_layout.setVerticalSpacing(10)
        
        self.scroll = QScrollArea()
        self.scroll.setContentsMargins(QMargins(0,0,0,0))
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll.setWidget(self.scroll_widget)
        
        self.pagebox.addWidget(self.scroll, 100, Qt.AlignmentFlag.AlignTop)

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll.setSizePolicy(sizePolicy)
        
        self.on_populate_tab(_name)
        
        ###### USER
        _name = "User"
        self.page2 = QWidget()
        
        self.gtab.addTab(self.page2, _name)
        self.pagebox2 = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.page2.setLayout(self.pagebox2)
        
        self.buttonbox2 = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.pagebox2.addLayout(self.buttonbox2)
        
        self.reload_btn2 = QPushButton("reload")
        self.reload_btn2.clicked.connect(self.on_reload)
        self.buttonbox2.addWidget(self.reload_btn2, 0, Qt.AlignmentFlag.AlignTop)
        
        self.quit_btn2 = QPushButton("exit")
        self.quit_btn2.clicked.connect(self.close)
        self.buttonbox2.addWidget(self.quit_btn2, 0, Qt.AlignmentFlag.AlignTop)
        
        self.scroll_widget2 = QWidget()
        self.scroll_widget2.setContentsMargins(QMargins(0,0,0,0))
        self.scroll_widget2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.scroll_layout2 = QGridLayout()
        self.scroll_layout2.setContentsMargins(QMargins(0,0,0,0))
        self.scroll_layout2.setSpacing(0)
        self.scroll_widget2.setLayout(self.scroll_layout2)
        self.scroll_layout2.setColumnStretch(3, 10)
        # self.scroll_layout2.setContentsMargins(QMargins(10,10,10,10))
        self.scroll_layout2.setHorizontalSpacing(10)
        self.scroll_layout2.setVerticalSpacing(10)
        
        self.scroll2 = QScrollArea()
        self.scroll2.setContentsMargins(QMargins(0,0,0,0))
        self.scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll2.setWidget(self.scroll_widget2)
        
        self.pagebox2.addWidget(self.scroll2, 1, Qt.AlignmentFlag.AlignTop)
        
        self.on_populate_tab(_name)
        
        
    def on_populate_tab(self, _name):
        if _name == "System":
            system_list = on_status_system()
            
            self.scroll_layout.addWidget(QLabel("SERVICE "), 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
            self.scroll_layout.addWidget(QLabel("STATE "), 0, 2, 1, 1, Qt.AlignmentFlag.AlignLeft)
            self.scroll_layout.addWidget(QLabel("STATUS "), 0, 3, 1, 1, Qt.AlignmentFlag.AlignLeft)
            
            i = 1
            for el in system_list:
                # _service_name = el[0].replace(".service","")
                _service_name = el[0].removesuffix(".service")
                _state = el[1]
                _status = el[2]
                
                _info_service = QPushButton(QIcon("icons/gear.png"), "")
                _info_service.setIconSize(QSize(int(BUTTON_SIZE/self.pixel_ratio), int(BUTTON_SIZE/self.pixel_ratio)))
                _info_service.uservice = [_service_name,_state,_status]
                _info_service.clicked.connect(self.on_info_service)
                self.scroll_layout.addWidget(_info_service, i, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
                self.scroll_layout.addWidget(QLabel(_service_name),i,1,1,1, Qt.AlignmentFlag.AlignLeft)
                self.scroll_layout.addWidget(QLabel(_state),i,2,1,1, Qt.AlignmentFlag.AlignLeft)
                self.scroll_layout.addWidget(QLabel(_status),i,3,1,1, Qt.AlignmentFlag.AlignLeft)
                
                i += 1
            
        elif _name == "User":
            user_list = on_status_user()
            
            self.scroll_layout2.addWidget(QLabel("SERVICE "), 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
            self.scroll_layout2.addWidget(QLabel("STATE "), 0, 2, 1, 1, Qt.AlignmentFlag.AlignLeft)
            self.scroll_layout2.addWidget(QLabel("STATUS "), 0, 3, 1, 1, Qt.AlignmentFlag.AlignLeft)
            
            i = 1
            for el in user_list:
                # _service_name = el[0].replace(".service","")
                _service_name = el[0].removesuffix(".service")
                _state = el[1]
                _status = el[2]
                
                _info_service = QPushButton(QIcon("icons/gear.png"), "")
                _info_service.setIconSize(QSize(int(BUTTON_SIZE/self.pixel_ratio), int(BUTTON_SIZE/self.pixel_ratio)))
                _info_service.uservice = [_service_name,_state,_status]
                _info_service.clicked.connect(self.on_info_service)
                self.scroll_layout2.addWidget(_info_service, i, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
                self.scroll_layout2.addWidget(QLabel(_service_name),i,1,1,1, Qt.AlignmentFlag.AlignLeft)
                self.scroll_layout2.addWidget(QLabel(_state),i,2,1,1, Qt.AlignmentFlag.AlignLeft)
                self.scroll_layout2.addWidget(QLabel(_status),i,3,1,1, Qt.AlignmentFlag.AlignLeft)
                
                i += 1
    
    
    def empty_tab(self):
        curr_idx = self.gtab.currentIndex()
        
        if curr_idx == 0:
            while self.scroll_layout.count():
                child = self.scroll_layout.takeAt(0)
                if child.widget():
                  child.widget().deleteLater()
            self.on_populate_tab("System")
                
        elif curr_idx == 1:
            while self.scroll_layout2.count():
                child = self.scroll_layout2.takeAt(0)
                if child.widget():
                  child.widget().deleteLater()
            self.on_populate_tab("User")
    
    def on_info_service(self):
        data = self.sender().uservice
        # if data[2] == "disabled":
            # MyDialog("Info", "Not possible.",self)
            # return
        serviceDialog(data, self)
        
    def on_reload(self):
        self.empty_tab()
        # curr_idx = self.gtab.currentIndex()
        # if curr_idx == 0:
            # self.empty_tab("System")
        # elif curr_idx == 1:
            # self.empty_tab("User")
    
    def resizeEvent(self, event):
        new_w = int(event.size().width()*self.pixel_ratio)
        new_h = int(event.size().height()*self.pixel_ratio)
        if new_w != int(WINW) or new_h != int(WINH):
            try:
                ifile = open("winsize.cfg", "w")
                ifile.write("{};{}".format(new_w, new_h))
                ifile.close()
            except Exception as E:
                MyDialog("Error", str(E), self)
    
    def closeEvent(self, event):
        app.instance().quit()


class serviceDialog(QDialog):
    def __init__(self, data, parent):
        super(serviceDialog, self).__init__(parent)
        # self.setWindowIcon(QIcon("icons/.svg"))
        self.setWindowTitle("Service Properties")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.resize(dialWidth,100)
        # data = [service name, state, status]
        self.data = data
        self.parent = parent
        #
        grid = QGridLayout()
        grid.setContentsMargins(5,5,5,5)
        #
        label0 = QLabel("<i>Service name: </i>")
        grid.addWidget(label0, 1, 0, Qt.AlignmentFlag.AlignLeft)
        label0_data = QLabel(data[0])
        grid.addWidget(label0_data, 1, 1, Qt.AlignmentFlag.AlignLeft)
        #
        lbl_desc = QLabel("<i>Description: </i>")
        grid.addWidget(lbl_desc, 2, 0, Qt.AlignmentFlag.AlignLeft)
        lbl_desc_desc = QLabel()
        lbl_desc_desc.setWordWrap(True)
        grid.addWidget(lbl_desc_desc, 2, 1, Qt.AlignmentFlag.AlignLeft)
        #
        label1 = QLabel("<i>State: </i>")
        grid.addWidget(label1, 3, 0, Qt.AlignmentFlag.AlignLeft)
        label1_data = QLabel(data[1])
        grid.addWidget(label1_data, 3, 1, Qt.AlignmentFlag.AlignLeft)
        #
        # label2 = QLabel("<i>Status: </i>")
        # grid.addWidget(label2, 4, 0, Qt.AlignmentFlag.AlignLeft)
        # label2_data = QLabel(data[2])
        # grid.addWidget(label2_data, 4, 1, Qt.AlignmentFlag.AlignLeft)
        #
        lbl_is_active = QLabel("<i>Is active: </i>")
        grid.addWidget(lbl_is_active, 4, 0, Qt.AlignmentFlag.AlignLeft)
        lbl_is_active_state = QLabel()
        grid.addWidget(lbl_is_active_state, 4, 1, Qt.AlignmentFlag.AlignLeft)
        #
        _description = ""
        active_state = -1
        can_start = None
        can_stop = None
        can_reload = None
        try:
            # can_start = subprocess.check_output(["systemctl","show","--property=CanStart", self.data[0]]).decode().strip("\n")
            # can_stop = subprocess.check_output(["systemctl","show","--property=CanStop", self.data[0]]).decode().strip("\n")
            # can_reload = subprocess.check_output(["systemctl","show","--property=CanReload", self.data[0]]).decode().strip("\n")
            can_actions = subprocess.check_output(["systemctl","show","--property=Description,ActiveState,CanStart,CanStop,CanReload", self.data[0]]).decode()
            tmp_actions = can_actions.split("\n")
            tmp_actions.remove('')
            _description = tmp_actions[0].split("=")[1]
            lbl_desc_desc.setText(_description)
            if "ActiveState=active" in tmp_actions:
                active_state = 1
                lbl_is_active_state.setText("active")
            elif "ActiveState=inactive" in tmp_actions:
                active_state = 0
                lbl_is_active_state.setText("inactive")
            if "CanStart=yes" in tmp_actions:
                can_start = 1
            if "CanStop=yes" in tmp_actions:
                can_stop = 1
            if "CanReload=yes" in tmp_actions:
                can_reload = 1
        except:
            pass
        
        _actions = ["Enable", "Disable", "Mask", "Unmask"]
        
        if can_reload:
            _actions.insert(0,"Reload")
        if can_start and can_stop:
            _actions.insert(0,"Restart")
            _actions.insert(0,"Stop")
            _actions.insert(0,"Start")
        
        #
        label3 = QLabel("<i>Action: </i>")
        grid.addWidget(label3, 5, 0, Qt.AlignmentFlag.AlignLeft)
        # label3_data = QLabel("")
        # grid.addWidget(label3_data, 5, 1, Qt.AlignmentFlag.AlignLeft)
        #
        self.action_combo = QComboBox()
        # self.action_combo.addItems(["Start","Restart","Reload","Stop","Enable", "Disable", "Mask", "Unmask"])
        self.action_combo.addItems(_actions)
        # self.action_combo.setCurrentIndex(0)
        grid.addWidget(self.action_combo, 5, 1, Qt.AlignmentFlag.AlignLeft)
        #
        action_btn = QPushButton("APPLY")
        action_btn.clicked.connect(self.on_apply)
        grid.addWidget(action_btn, 5, 2, Qt.AlignmentFlag.AlignLeft)
        #
        button_ok = QPushButton("   Close   ")
        grid.addWidget(button_ok, 12, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(grid)
        button_ok.clicked.connect(self.close)
        self.exec()
    
    def on_apply(self):
        state_choise = self.action_combo.currentText().lower()
        
        if state_choise == self.data[1][0:-1].lower():
            MyDialog("Error", "Same state.", self)
            return
        elif state_choise == "unmask" and self.data[1].lower() != "masked":
            MyDialog("Error", "Unmask not possible.", self)
            return
        elif state_choise == "enable" and self.data[1].lower() == "masked":
            MyDialog("Error", "Unmask first.", self)
            return
        elif state_choise in ["start","restart","reload","stop"] and self.data[1].lower() in ["disabled","masked"]:
            MyDialog("Error", "The service is disabled or masked.", self)
            return
        else:
            ret = -1
            is_user_service = 0
            if os.path.exists(os.path.join(MY_HOME,".config/systemd/user",self.data[0]+".service")):
                is_user_service = 1
            try:
                if os.geteuid() != 0:
                    if is_user_service == 0:
                        # 0 success
                        ret = subprocess.call(["pkexec","systemctl",state_choise,self.data[0]])
                    else:
                        # 0 success
                        ret = subprocess.call(["systemctl","--user",state_choise,self.data[0]])  
                else:
                    # 0 success
                    ret = subprocess.call(["systemctl",state_choise,self.data[0]])
            except:
                ret = -1
            if ret == 0:
                MyDialog("Info", "Done.", self)
                self.parent.empty_tab()
                self.close()
            elif ret == -1:
                MyDialog("Error", "Error in the command line.", self)
                self.close()
            else:
                MyDialog("Error", "Error.", self)
                self.close()


# type - message - parent
class MyDialog(QMessageBox):
    def __init__(self, *args):
        super(MyDialog, self).__init__(args[-1])
        if args[0] == "Info":
            self.setIcon(QMessageBox.Icon.Information)
            self.setStandardButtons(QMessageBox.StandardButton.Ok)
        elif args[0] == "Error":
            self.setIcon(QMessageBox.Icon.Critical)
            self.setStandardButtons(QMessageBox.StandardButton.Ok)
        elif args[0] == "Question":
            self.setIcon(QMessageBox.Icon.Question)
            self.setStandardButtons(QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)
        # self.setWindowIcon(QIcon("icons/.svg"))
        self.setWindowTitle(args[0])
        self.resize(dialWidth,100)
        self.setText(args[1])
        retval = self.exec()
    
    def event(self, e):
        result = QMessageBox.event(self, e)
        #
        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)
        self.setMinimumWidth(0)
        self.setMaximumWidth(16777215)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # 
        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    if use_font_size:
        app.setStyleSheet("QWidget{font-size:"+f"{use_font_size}"+"px;}")
    
    window = MainWin()
    window.show()
    ret = app.exec()
    sys.exit(ret)
