import os
import sys
import json
import subprocess

import psutil


def get_version_and_user_data_path():
    os_and_user_data_paths = {
        'win32': {
            'stable': '~/AppData/Local/Microsoft/Edge/User Data',
            'canary': '~/AppData/Local/Microsoft/Edge Canary/User Data',
            'dev': '~/AppData/Local/Microsoft/Edge Dev/User Data',
            'beta': '~/AppData/Local/Microsoft/Edge Beta/User Data',
        },
        'linux': {
            'stable': '~/.config/microsoft-edge',
            'canary': '~/.config/microsoft-edge-canary',
            'dev': '~/.config/microsoft-edge-dev',
            'beta': '~/.config/microsoft-edge-beta',
        },
        'darwin': {
            'stable': '~/Library/Application Support/Microsoft Edge',
            'canary': '~/Library/Application Support/Microsoft Edge Canary',
            'dev': '~/Library/Application Support/Microsoft Edge Dev',
            'beta': '~/Library/Application Support/Microsoft Edge Beta',
        },
    }

    for platform, version_and_user_data_path in os_and_user_data_paths.items():
        available_version_and_user_data_path = {}
        if sys.platform.startswith(platform):
            for version, user_data_path in version_and_user_data_path.items():
                user_data_path = os.path.abspath(os.path.expanduser(user_data_path))
                if os.path.exists(user_data_path):
                    available_version_and_user_data_path[version] = user_data_path
            return available_version_and_user_data_path

    raise Exception('Unsupported platform %s' % sys.platform)


def shutdown_edge():
    terminated_edges = set()
    for process in psutil.process_iter():
        try:
            if sys.platform == 'darwin':
                if not process.name().startswith('Microsoft Edge'):
                    continue
            elif os.path.splitext(process.name())[0] != 'msedge':
                continue
            elif not process.is_running():
                continue
            elif process.parent() is not None and process.parent().name() == process.name():
                continue
            location = process.exe()
            process.kill()
            terminated_edges.add(location)
        except psutil.NoSuchProcess:
            pass
    return terminated_edges


def get_last_version(user_data_path):
    last_version_file = os.path.join(user_data_path, 'Last Version')
    if not os.path.exists(last_version_file):
        return None
    with open(last_version_file, 'r', encoding='utf-8') as fp:
        return fp.read()


def patch_local_state(user_data_path):
    local_state_file = os.path.join(user_data_path, 'Local State')
    if not os.path.exists(local_state_file):
        print('Failed to patch Local State. File not found', local_state_file)

    with open(local_state_file, 'r', encoding='utf-8') as fp:
        local_state = json.load(fp)

    if local_state['variations_country'] != 'US':
        local_state['variations_country'] = 'US'
        with open(local_state_file, 'w', encoding='utf-8') as fp:
            json.dump(local_state, fp)
        print('Succeeded in patching Local State')
    else:
        print('No need to patch Local State')


def patch_preferences(user_data_path):
    for file in os.listdir(user_data_path):
        if not os.path.isdir(file) and file != 'Default' and not file.startswith('Profile '):
            continue

        preferences_file = os.path.join(user_data_path, file, 'Preferences')
        with open(preferences_file, 'r', encoding='utf-8') as fp:
            preferences = json.load(fp)

        if preferences['browser'].get('chat_ip_eligibility_status') in [None, False]:
            preferences['browser']['chat_ip_eligibility_status'] = True
            with open(preferences_file, 'w', encoding='utf-8') as fp:
                json.dump(preferences, fp)
            print('Succeeded in patching Preferences of', file)
        else:
            print('No need to patch Preferences of', file)


def main():
    version_and_user_data_path = get_version_and_user_data_path()
    if len(version_and_user_data_path) == 0:
        raise Exception('No available user data path found')

    terminated_edges = shutdown_edge()
    if len(terminated_edges) > 0:
        print('Shutdown Edge')

    for version, user_data_path in version_and_user_data_path.items():
        last_version = get_last_version(user_data_path)
        if last_version is None:
            print('Failed to get version. File not found', os.path.join(user_data_path, 'Last Version'))
            continue
        main_version = int(last_version.split('.')[0])
        print('Patching Edge', version, last_version, '"'+user_data_path+'"')
        if main_version == 120:
            patch_local_state(user_data_path)
        elif main_version >= 121:
            patch_preferences(user_data_path)
        else:
            patch_local_state(user_data_path)
            patch_preferences(user_data_path)

    if len(terminated_edges) > 0:
        print('Restart Edge')
        for edge in terminated_edges:
            subprocess.Popen([edge, '--start-maximized'], stderr=subprocess.DEVNULL)

    input('Enter to continue...')


if __name__ == '__main__':
    main()
