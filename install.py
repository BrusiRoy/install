import colorama
import os
from pathlib import Path
import platform
import shutil
import sys
import yaml

colorama.init()

def print_ok(msg):
    print(f'{colorama.Fore.GREEN}[OK] {colorama.Style.RESET_ALL}{msg}')

def print_warn(msg):
    print(f'{colorama.Fore.YELLOW}[WARN] {colorama.Style.RESET_ALL}{msg}')

def print_error(msg):
    print(f'{colorama.Fore.RED}[ERROR] {colorama.Style.RESET_ALL}{msg}')
    exit(1)


class Config:
    def __init__(self, config_file_path):
        # Load the config file
        with open(config_file_path, 'r') as stream:
            try:
                config = yaml.load(stream)
            except Exception:
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
                print_error(f'Current platform ({current_platform}) not found in `{config_file_path}`')

        else:
            print_error(f'Missing tag `platform` in `{config_file_path}`')

        self._convert_home_tilde()


    def _convert_home_tilde(self):
        """Converts the '~' in the path by the actual HOME path"""
        self.src = [src.replace('~', str(Path.home())) for src in self.src]
        self.dest = [dest.replace('~', str(Path.home())) for dest in self.dest]

    def _file_exists(self, src, dest):
        # TODO: More input validation
        # TODO: Add more options, like move to a `.old` file
        print_warn(f'File `{dest}` already exists... Do you want to remove it? (y/N)')
        variable = str(input()).lower().strip()
        if variable == 'y':
            self._copy_file(src, dest)
        elif variable == 'n' or variable == '':
            # TODO:
            pass
        else:
            print_error('Invalid input')

    def _copy_file(self, src, dest):
        shutil.copy2(src, dest)
        print_ok(f'Successfully copied `{src}` to `{dest}`')

    def install(self):
        print(f'Installing {self.name} on the {self.platform} platform')
        for src, dest in zip(self.src, self.dest):
            if os.path.isfile(dest):
                self._file_exists(src, dest)
            else:
                self._copy_file(src, dest)


config = Config('config_example.yaml')
config.install()

