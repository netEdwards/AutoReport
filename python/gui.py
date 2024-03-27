import playwrightcollection as ps
import PySimpleGUI as sg
from functions import get_excel_path, set_excel_path
import threading
import time
import os
import sys

def set_playwright_browsers_path():
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundled executable, the driver is in the extracted folder
        application_path = sys._MEIPASS
    else:
        # If it's run in a normal Python environment, __file__ contains the path to the script
        application_path = os.path.dirname(__file__)
    
    # Adjust the relative path below according to your directory structure
    browsers_path = os.path.join(application_path, "playwrightbrowsers")
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = browsers_path

# Make sure to call this function before importing or using Playwright
set_playwright_browsers_path()


def threaded_main(window, cancel_event):
    try:
        cancel_event.clear()
        ps.main(cancel_event)
        window['-STATE-'].update('State: [IDLE]')
    except Exception as e:
        print(f"Thread Error: {e}")
        window['-STATE-'].update('State: [ERROR]')
    
themes = sg.theme_list()

def create_window(theme):
    sg.theme(theme)
    layout = [
        [sg.Text('Hello this is a python script that will automate a report off of eRQA for Chick-fil-A', font=('Helvetica', 13), auto_size_text=True, justification='center', expand_x=True)],
        [sg.Text('Below is a button to execute the script, and then a button to cancel it. I will display a console log, which you can toggle.', font=('Helvetica', 13), auto_size_text=True, justification='center', expand_x=True)],
        [sg.Text('Please do not close the window while the script is running, or any windows that may popup.', font=('Helvetica', 13), auto_size_text=True, justification='center', expand_x=True)],
        [sg.Text('Aslo, please note this website is a bit unstable so sometimes things dont load, if that happens just hit run again after a few seconds.', font=('Helvetica', 13), auto_size_text=True, justification='center', expand_x=True)],
        [sg.Text('State: [IDLE]', key='-STATE-')],
        [sg.Button('Run', key='-RUN-'), sg.Button('Cancel', key='-CANCEL-')],
        [sg.Multiline(size=(100, 20), key='-OUTPUT-', background_color='black', text_color='white', horizontal_scroll=False, autoscroll=True, echo_stdout_stderr=True, reroute_stdout=True, reroute_cprint=True, justification='center', expand_x=True)],
        [sg.Button('Toggle Console Log', key='-TOGGLE-'), sg.Text('Change file path: '), sg.Input(f"{get_excel_path()}", key='-INPUT-'), sg.FolderBrowse('Browse', key="BROW-"), sg.Button("🔁", key='-REFRESH-')],
        [sg.Text(f'Excel File Path: {get_excel_path()}/[EXCEL FILE]', key='-PATH-')],
        [sg.Button('Exit', key='-EXIT-'), sg.DropDown(themes, key='-THEME-', default_value=theme, enable_events=True, size=(20, 20), auto_size_text=True, expand_x=True, expand_y=True, font=('Helvetica', 13))]
    ]
    return sg.Window('AutoReport', layout, icon='python/media/Bot.ico', finalize=True)


def main():
    window = create_window('Topanga')
    toggle_console = True
    cancel_event = threading.Event()
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-RUN-':
            if get_excel_path() != '':
                threading.Thread(target=threaded_main, args=(window, cancel_event), daemon=True).start()
                window['-STATE-'].update('State: [RUNNING]')
            else:
                sg.popup("Please select a file path to save the excel file & CLICK RELOAD Button!")
        if event == '-CANCEL-':
            print("Sending cancel request...")
            cancel_event.set()
            window['-STATE-'].update('State: [CLOSING..]')
            time.sleep(1)
            window['-STATE-'].update('State: [IDLE]')
        if event == '-TOGGLE-':
            if toggle_console:
                window['-OUTPUT-'].update(visible=False)
                toggle_console = False
            else:
                window['-OUTPUT-'].update(visible=True)
                toggle_console = True
        if event == '-REFRESH-':
            set_excel_path(values["BROW-"])
            window['-PATH-'].update(f'Excel File Path: {get_excel_path()}/[EXCEL FILE]')
        if event == '-THEME-':
            window.close()
            window = create_window(values['-THEME-'])
        if event == '-EXIT-':
            window.close()
            exit
    window.close()


if __name__ == '__main__':
    main()
