import colorama
import platform
import yaml

colorama.init()

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


config = Config('config_example.yaml')

