#!/usr/bin/env python3

# version 0.4

USE_STATIC = 1 # 0: do not search for services in static state; 1: does
BUTTON_SIZE = 48
dialWidth = 400 # dialog width
RESIZE_HANDLING = 1 # 0 to disable the window resizing and to use the following sizes
WINW = 800
WINH = 600

import sys,os
import subprocess
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Pango

MY_HOME = os.path.expanduser('~')

WINW = 800
WINH = 600

if RESIZE_HANDLING:
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
            print("Error: The file winsize.cfg cannot be read/created.")
            sys.exit()


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

def MyDialog(data1, data2, parent):
    dialog = Gtk.AlertDialog()
    dialog.set_message(data1)
    dialog.set_detail(data2)
    dialog.set_modal(True)
    dialog.set_buttons(["Close"])
    dialog.show(parent)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_ = self.get_application()
        
        self.set_title("ServicesGtk4")
        self.set_size_request(WINW,WINH)
        
        self.main_box = Gtk.Box.new( Gtk.Orientation.VERTICAL,10)
        self.set_child(self.main_box)
        
        ### main buttons
        self.box_btn = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        self.main_box.append(self.box_btn)
        
        self.reload_btn = Gtk.Button.new()
        self.reload_btn.set_label("Reload")
        self.reload_btn.connect("clicked",self.on_reload)
        self.reload_btn.props.hexpand = True 
        self.box_btn.append(self.reload_btn)

        self.quit_button = Gtk.Button.new_with_label("Quit")
        self.quit_button.connect("clicked",self.on_quit)
        self.quit_button.props.hexpand = True 
        self.box_btn.append(self.quit_button)
        
        ######### SYSTEM/USER
        self.notebook = Gtk.Notebook.new()
        self.main_box.append(self.notebook)
        
        #### system
        self.scroll1 = Gtk.ScrolledWindow.new()
        self.scroll1.props.vexpand = True
        self.scroll1.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scroll1.set_placement(Gtk.CornerType.TOP_LEFT)
        self.notebook.append_page(self.scroll1, Gtk.Label(label="System"))
        
        self.grid1 = Gtk.Grid.new()
        self.grid1.props.vexpand = True
        self.grid1.set_column_spacing(10)
        self.scroll1.set_child(self.grid1)
        
        self.num_rows1 = 0
        
        # populate
        self.populate_services("system")
        
        ##### user
        self.scroll2 = Gtk.ScrolledWindow.new()
        self.scroll2.props.vexpand = True
        self.scroll2.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scroll2.set_placement(Gtk.CornerType.TOP_LEFT)
        self.notebook.append_page(self.scroll2, Gtk.Label(label="User"))
        
        self.grid2 = Gtk.Grid.new()
        self.grid2.props.vexpand = True
        self.grid2.set_column_spacing(10)
        self.scroll2.set_child(self.grid2)
        
        self.num_rows2 = 0
        
        # populate
        self.populate_services("user")
        
        self.surface_id_connect = None
        self.old_width = None
        self.old_height = None
        
        self.connect("show", self.on_show)
    
    def on_surface(self, aa,ww,hh):
        self.old_width = self.get_width()
        self.old_height = self.get_height()
        aa.disconnect(self.surface_id_connect)
        self.surface_id_connect = None
    
    def on_show(self, w):
        self._surface = self.get_surface()
        self.surface_id_connect = self._surface.connect("layout",self.on_surface)
    
    def populate_services(self, _name):
        if _name == "system":
            system_list = on_status_system()
            
            self.grid1.attach(self.on_label_new("SERVICE"), 1, 0, 1, 1)
            self.grid1.attach(self.on_label_new("STATE"), 2, 0, 1, 1)
            self.grid1.attach(self.on_label_new("STATUS"), 3, 0, 1, 1)
            
            i = 1
            for el in system_list:
                # _service_name = el[0].replace(".service","")
                _service_name = el[0].removesuffix(".service")
                _state = el[1]
                _status = el[2]
                
                _info_service = Gtk.Button.new()
                img = Gtk.Image.new_from_file("icons/gear.png")
                img.set_pixel_size(BUTTON_SIZE)
                _info_service.set_child(img)
                _info_service.uservice = [_service_name,_state,_status]
                _info_service.connect("clicked",self.on_info_service)
                self.grid1.attach(_info_service, 0, i, 1, 1)
                self.grid1.attach(self.on_label_new(_service_name),1,i,1,1)
                self.grid1.attach(self.on_label_new(_state),2,i,1,1)
                self.grid1.attach(self.on_label_new(_status),3,i,1,1)
                
                i += 1
            
            self.num_rows1 = i+1
            
        elif _name == "user":
            user_list = on_status_user()
            
            self.grid2.attach(self.on_label_new("SERVICE"), 1, 0, 1, 1)
            self.grid2.attach(self.on_label_new("STATE"), 2, 0, 1, 1)
            self.grid2.attach(self.on_label_new("STATUS"), 3, 0, 1, 1)
            
            i = 1
            for el in user_list:
                # _service_name = el[0].replace(".service","")
                _service_name = el[0].removesuffix(".service")
                _state = el[1]
                _status = el[2]
                
                _info_service = Gtk.Button.new()
                img = Gtk.Image.new_from_file("icons/gear.png")
                img.set_pixel_size(BUTTON_SIZE)
                _info_service.set_child(img)
                _info_service.uservice = [_service_name,_state,_status]
                _info_service.connect("clicked",self.on_info_service)
                self.grid2.attach(_info_service, 0, i, 1, 1)
                self.grid2.attach(self.on_label_new(_service_name),1,i,1,1)
                self.grid2.attach(self.on_label_new(_state),2,i,1,1)
                self.grid2.attach(self.on_label_new(_status),3,i,1,1)
                
                i += 1
            
            self.num_rows2 = i+1
    
    
    def on_label_new(self, _str):
        lbl = Gtk.Label(label=_str)
        lbl.props.halign = True
        return lbl
    
    def on_info_service(self, btn):
        data = btn.uservice
        # if data[2] == "disabled":
            # MyDialog("Info", "Not possible.",self)
            # return
        serviceDialog(self, data)
    
    def on_reload(self, btn):
        self.empty_tab()
    
    def empty_tab(self):
        curr_idx = self.notebook.get_current_page()
        if curr_idx == 0:
            for i in range(self.num_rows1):
                self.grid1.remove_row(0)
            self.populate_services("system")
        elif curr_idx == 1:
            for i in range(self.num_rows2):
                self.grid2.remove_row(0)
            self.populate_services("user")
    
    
    def on_quit(self,btn):
        if RESIZE_HANDLING:
            new_w = self.get_width()
            new_h = self.get_height()
            if new_w != self.old_width or new_h != self.old_height :
                w_pad = int(WINW-self.old_width)
                h_pad = int(WINH-self.old_height)
                try:
                    ifile = open("winsize.cfg", "w")
                    ifile.write("{};{}".format(new_w+w_pad, new_h+h_pad))
                    ifile.close()
                except Exception as E:
                    MyDialog("Error", str(E), self)
        
        self.app_.quit()

# title - body - parent
class MyDialog1(Gtk.Window):
    def __init__(self, data1, data2, parent):
        super().__init__()
        
        self.data1 = data1
        self.data2 = data2
        self._parent = parent
        self.set_transient_for(self._parent)
        self.set_modal(True)
        self.set_title(self.data1)
        
        self.main_box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL,spacing=0)
        self.set_child(self.main_box)
        
        lbl2 = Gtk.Label(label=self.data2)
        self.main_box.append(lbl2)
        
        btn1 = Gtk.Button(label="Close")
        self.main_box.append(btn1)
        btn1.connect("clicked",self.on_close)
        
        self.present()
        
    def on_close(self, btn):
        self.close()
    

class serviceDialog(Gtk.Window):
    def __init__(self, parent, data):
        super().__init__()
        
        self.data = data
        self._parent = parent
        self.set_transient_for(self._parent)
        self.set_modal(True)
        self.set_title("Manager")
        
        self.set_size_request(dialWidth,-1)
        
        self.main_box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL,spacing=0)
        # _pad = 10
        # self.main_box.set_margin_start(_pad)
        # self.main_box.set_margin_end(_pad)
        self.set_child(self.main_box)
        
        self.grid = Gtk.Grid.new()
        self.main_box.append(self.grid)
        
        lbl_sn = Gtk.Label(label=" Service name: ")
        lbl_sn.props.halign = True
        self.grid.attach(lbl_sn,0,0,1,1)
        lbl_sn_name = Gtk.Label(label=self.data[0])
        lbl_sn_name.props.halign = True
        self.grid.attach(lbl_sn_name,1,0,1,1)
        
        lbl_desc = Gtk.Label(label=" Description: ")
        lbl_desc.props.halign = True
        self.grid.attach(lbl_desc,0,1,1,1)
        lbl_desc_desc = Gtk.Label(label="")
        lbl_desc_desc.props.halign = True
        lbl_desc_desc.set_wrap(True)
        lbl_desc_desc.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        self.grid.attach(lbl_desc_desc,1,1,30,1)
        
        lbl_state = Gtk.Label(label=" State: ")
        lbl_state.props.halign = True
        self.grid.attach(lbl_state,0,2,1,1)
        lbl_state_name = Gtk.Label(label=self.data[1])
        lbl_state_name.props.halign = True
        self.grid.attach(lbl_state_name,1,2,1,1)
        
        # lbl_status = Gtk.Label(label=" Status: ")
        # lbl_status.props.halign = True
        # self.grid.attach(lbl_status,0,3,1,1)
        # lbl_status_name = Gtk.Label(label=self.data[2])
        # lbl_status_name.props.halign = True
        # self.grid.attach(lbl_status_name,1,3,1,1)
        
        lbl_is_active = Gtk.Label(label=" Is active: ")
        lbl_is_active.props.halign = True
        self.grid.attach(lbl_is_active,0,4,1,1)
        # is_active = None
        # try:
            # rett = subprocess.check_output(["systemctl","is-active",self.data[0]])#.decode()#.strip("\n")
        # except:
            # pass
        lbl_is_active_state = Gtk.Label(label="")
        lbl_is_active_state.props.halign = True
        self.grid.attach(lbl_is_active_state,1,4,1,1)
        
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
            lbl_desc_desc.set_text(_description)
            if "ActiveState=active" in tmp_actions:
                active_state = 1
                lbl_is_active_state.set_text("active")
            elif "ActiveState=inactive" in tmp_actions:
                active_state = 0
                lbl_is_active_state.set_text("inactive")
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
        if can_stop:
            _actions.insert(0,"Stop")
        if can_start:
            _actions.insert(0,"Start")
        
        lbl_action = Gtk.Label(label=" Action: ")
        lbl_action.props.halign = True
        self.grid.attach(lbl_action,0,5,1,1)
        self._dropdown1 = Gtk.DropDown.new_from_strings(_actions)
        self.grid.attach(self._dropdown1,1,5,1,1)
        btn_apply = Gtk.Button(label="Apply")
        self.grid.attach(btn_apply,2,5,1,1)
        btn_apply.connect("clicked", self.on_btn_apply)
        
        self.lbl_msg = Gtk.Label(label="")
        self.main_box.append(self.lbl_msg)
        
        quit_btn = Gtk.Button(label="Close")
        quit_btn.connect("clicked", self.on_close)
        self.main_box.append(quit_btn)
        
        self.present()
        
    def on_btn_apply(self, btn):
        state_choise = self._dropdown1.get_selected_item().props.string.lower()
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
            except Exception as E:
                # MyDialog("Error", str(E), self)
                self.lbl_msg.set_text("Error.")
                # self.close()
                # ret = -1
            if ret == 0:
                # MyDialog("Info", "Done.", self)
                # self.lbl_msg.set_text("Done.")
                self._parent.empty_tab()
                self.close()
            # elif ret == -1:
                # MyDialog("Error", "Error in the command line.", self)
                # self.close()
            else:
                # MyDialog("Error", "Error:\n{}".format(str(ret)), self)
                self.lbl_msg.set_text("Error.")
                # self.close()
    
    def on_close(self, event):
        self.close()
        
class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def do_activate(self):
        active_window = self.props.active_window
        if active_window:
            active_window.present()
        else:
            self.win = MainWindow(application=self)
            self.win.present()


app = MyApp()
app.run(sys.argv)
