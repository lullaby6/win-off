import os, time, subprocess, sys, winreg, ctypes

if not sys.platform == 'win32':
    input('WinOff is only for Windows. If you have Windows make sure you have the correct version of Windows installed.')
    sys.exit()

def run_as_admin():
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            sys.exit()
    except Exception as e:
        input(f"An error occurred while elevating administrator privileges: {str(e)}")
        sys.exit()

run_as_admin()

def run_command_as_admin(command):
    return subprocess.run(command.split(' '), capture_output=True, shell=True, text=True)

version = '1.0.0'

os.system(f'title WinOff v{version}')

def disable_sysmain():
    os.system('sc stop SysMain')
    os.system('sc config SysMain start=disabled')

def disable_wpnservice():
    os.system('sc stop WpnService')
    os.system('sc config WpnService start=disabled')

def disable_windows_search():
    os.system('sc stop "wsearch"')
    os.system('sc config "wsearch" start=disabled')

def shutdown():
    os.system('shutdown -s -t 05')

def disable_fast_boot():
    os.system('reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Power" /v HiberbootEnabled /t reg_dword /d 0 /f')

def disable_transparency():
    os.system('reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize /v EnableTransparency /t REG_DWORD /d 0 /f')

def disable_visual_effects():
    os.system('reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects /v VisualFXSetting /t REG_DWORD /d 2 /f')

def clear_temp_files():
    os.system('cd %TEMP% && del /F /Q *.*')
    os.system('cd %SystemRoot%\Temp && del /F /Q *.*')

def unlock_ultimate_performance_power_plan():
    os.system('powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61')

def enable_platform_tick():
    os.system('bcdedit /set useplatformtick yes')

def reset_platform_tick():
    os.system('bcdedit /deletevalue useplatformtick')

def enable_dynamic_tick():
    os.system('bcdedit /set disabledynamictick yes')

def reset_dynamic_tick():
    os.system('bcdedit /deletevalue disabledynamictick')

def enable_hpet():
    os.system('bcdedit /set useplatformclock true')

def reset_hpet():
    os.system('bcdedit /deletevalue useplatformclock')

def clear_dns_cache():
    os.system('ipconfig /flushdns')
    os.system('ipconfig /registerdns')
    os.system('ipconfig /release')
    os.system('ipconfig /renew')
    os.system('netsh winsock reset')

def disable_hibernation():
    os.system('powercfg.exe /hibernate off')

# def set_high_performance_power_plan():
#     output = run_command_as_admin('powercfg -list').stdout

#     if 'Alto rendimiento' in output:
#         start_index = output.index('Alto rendimiento')
#         end_index = output.index('\n', start_index)
#         plan_line = output[start_index:end_index]
#         plan_guid = plan_line.split()[3]
#         run_command_as_admin(f'powercfg -setactive {plan_guid}')
#         print("The 'Alto rendimiento' power plan has been activated.")
#     elif 'High Performance' in output:
#         start_index = output.index('High Performance')
#         end_index = output.index('\n', start_index)
#         plan_line = output[start_index:end_index]
#         plan_guid = plan_line.split()[3]
#         run_command_as_admin(f'powercfg -setactive {plan_guid}')
#         print("The 'High Performance' power plan has been activated.")
#     else:
#         print("The 'High Performance' power plan was not found.")

# def disable_fast_boot():
    # try:
    #     key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Power"
    #     value_name = "HiberbootEnabled"
    #     value_data = 0

    #     key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)

    #     winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)

    #     winreg.CloseKey(key)

    #     print("[Regedit] Fast boot disabled.")
    # except Exception as e:
    #     print(f"[Regedit] An error occurred while disabling fast boot: {str(e)}")

def disable_telemetry():
    try:
        os.system('sc stop DiagTrack')
        os.system('sc config DiagTrack start=disabled')
    except Exception as e:
        print(f"[Service] An error occurred while disabling Telemetry: {str(e)}")

    try:
        key_path = r"SOFTWARE\Policies\Microsoft\Windows\DataCollection"
        value_name = "AllowTelemetry"
        value_data = 0

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)

        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)

        winreg.CloseKey(key)

        print("[Regedit] Telemetry has been deactivated correctly.")
    except FileNotFoundError:
        print("[Regedit] An error occurred while disabling Telemetry: The registry key does not exist. Make sure you have the correct version of Windows installed.")

def disable_windows_defender():
    try:
        run_command_as_admin('sc stop WinDefend')
        run_command_as_admin('sc config WinDefend start=disabled')

        print("[Service] Windows Defender disabled.")
    except Exception as e:
        print(f"[Service] An error occurred while disabling Windows Defender: {str(e)}")

    try:
        key_path = r"SOFTWARE\Policies\Microsoft\Windows Defender"
        value_name = "DisableAntiSpyware"
        value_data = 1

        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)

        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)

        winreg.CloseKey(key)

        print("[Regedit] Windows Defender disabled.")
    except Exception as e:
        print(f"[Regedit] An error occurred while disabling Windows Defender: {str(e)}")

menu = {
    'Disable SysMain/Superfetch/Prefetch': disable_sysmain,
    'Disable WPN Service': disable_wpnservice,
    'Disable Telemetry': disable_telemetry,
    'Disable Windows Search': disable_windows_search,
    'Disable Fast Boot': disable_fast_boot,
    'Disable Transparency': disable_transparency,
    'Disable Visual Effects': disable_visual_effects,
    'Disable Windows Defender (Try)': disable_windows_defender,
    'Disable Hibernation': disable_hibernation,
    'Enable Platform Tick': enable_platform_tick,
    'Reset Platform Tick': reset_platform_tick,
    'Enable Dynamic Tick': enable_dynamic_tick,
    'Reset Dynamic Tick': reset_dynamic_tick,
    'Enable High Precision Event Timer (HPET)': enable_hpet,
    'Reset High Precision Event Timer (HPET)': reset_hpet,
    'Unlock Ultimate Performance Power Plan': unlock_ultimate_performance_power_plan,
    'Clear DNS Cache': clear_dns_cache,
    'Clear Temp Files': clear_temp_files,
    'Shutdown': shutdown,
    'Exit': lambda: sys.exit()
}

while True:
    os.system('cls')
    print(f'WinOff v{version} - github.com/lullaby6/win-off\n')

    menu_keys = list(menu.keys())
    for index, option in enumerate(menu_keys):
        print(f'{index+1} - {option}')

    selected_option = input('\nSelect option: ')

    if selected_option.isdigit() and int(selected_option) > 0 and int(selected_option) <= len(menu_keys):
        key_selected = menu_keys[int(selected_option)-1]
        try:
            menu[key_selected]()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        input('\n>>> Press ENTER to continue')