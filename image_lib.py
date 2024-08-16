import subprocess
import platform

def set_desktop_background_image(image_path):
    system = platform.system()
    if system == 'Darwin':  # macOS
        try:
            # Use AppleScript to set the desktop background
            script = f'''
            osascript -e 'tell application "Finder" to set desktop picture to POSIX file "{image_path}"'
            '''
            subprocess.run(script, shell=True, check=True)
            print(f'Successfully set desktop to {image_path}')
        except subprocess.CalledProcessError:
            print(f'Failed to set desktop to {image_path}')
    else:
        print(f'Setting desktop background is not implemented for {system}')
