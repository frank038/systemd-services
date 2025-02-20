# systemd-services
Simple application for managing the systemd services.

Free to use and modify.

Requirements:
- python3
- pyqt6 (qt6 version)
- gir1.2-gtk-4.0 (gtk4 version)
- systemctl and pkexec

This application is just an attempt, and the user must know how to manage systemd. Usually, the commands stop, start, disable, mask, etc. are straightforward to understand.

Just execute the file systemd-services-qt6.py. This application uses only the command line program systemctl.

It seems a services should be first disabled, then stopped (and viceversa). 

![My image](https://github.com/frank038/systemd-services/blob/main/screenshot02.png)

![My image](https://github.com/frank038/systemd-services/blob/main/screenshot01.png)
