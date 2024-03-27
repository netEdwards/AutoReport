import PySimpleGUI as sg
available_themes = sg.theme_list()

print("Available Themes:")
for theme in available_themes:
    print(theme)