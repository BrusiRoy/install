"""Main install code"""
import os
from pathlib import Path
import platform
import shutil
import yaml

import colorama

colorama.init()

def print_ok(msg):
    """Print a `msg` with a green '[OK]' in front"""
    print(f'{colorama.Fore.GREEN}[OK] {colorama.Style.RESET_ALL}{msg}')

def print_warn(msg):
    """Print a `msg` with a yellow '[WARN]' in front"""
    print(f'{colorama.Fore.YELLOW}[WARN] {colorama.Style.RESET_ALL}{msg}')

def print_error(msg):
    """Print a `msg` with a red '[ERROR]' in front"""
    print(f'{colorama.Fore.RED}[ERROR] {colorama.Style.RESET_ALL}{msg}')
    exit(1)


class Config:
    """Represents an installation configuration"""
    def __init__(self, root_path, file_name):
        config_file_path = root_path + file_name
        self.root_path = root_path

        # Load the config file
        with open(config_file_path, 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError:
                print_error(f'Invalid YAML structure in `{config_file_path}`')

        # Save the name
        if 'name' in config:
            self.name = config['name']
        else:
            print_error(f'Missing tag `name` in `{config_file_path}`')

        # Look for the platform
        if 'platform' in config:
            current_platform = platform.system()

            if current_platform in config['platform']:
                self.platform = current_platform

                if 'src' in config['platform'][current_platform]:
                    self.src = config['platform'][current_platform]['src']
                else:
                    print_error(f'Missing tag `src` in `{config_file_path}`')

                if 'dest' in config['platform'][current_platform]:
                    self.dest = config['platform'][current_platform]['dest']
                else:
                    print_error(f'Missing tag `dest` in `{config_file_path}`')

            else:
                print_error(f'Current platform ({current_platform}) not \
                            found in `{config_file_path}`')

        else:
            print_error(f'Missing tag `platform` in `{config_file_path}`')

        self._convert_home_tilde()


    def _convert_home_tilde(self):
        """Converts the '~' in the path by the actual HOME path"""
        self.src = [self.root_path + src.replace('~', str(Path.home())) for src in self.src]
        self.dest = [dest.replace('~', str(Path.home())) for dest in self.dest]

    def _file_exists(self, src, dest):
        # FIXME: More input validation
        # FIXME: Add more options, like move to a `.old` file
        print_warn(f'File `{dest}` already exists... Do you want to remove it? (y/N)')
        variable = str(input()).lower().strip()
        if variable == 'y':
            self._copy_file(src, dest)
        elif variable == 'n' or variable == '':
            # FIXME:
            pass
        else:
            print_error('Invalid input')

    @staticmethod
    def _copy_file(src, dest):
        """Copy file `src` to `dest`"""
        shutil.copy2(src, dest)
        print_ok(f'Successfully copied `{src}` to `{dest}`')

    def install(self):
        """Start executing the installation steps of this configuration file"""
        print(f'Installing {self.name} on the {self.platform} platform')
        for src, dest in zip(self.src, self.dest):
            if os.path.isfile(dest):
                self._file_exists(src, dest)
            else:
                self._copy_file(src, dest)

for root, dirs, files in os.walk('dotfiles/'):
    for file in files:
        if 'install' in file and file.endswith('.yaml'):
            Config(root + '/', file).install()
