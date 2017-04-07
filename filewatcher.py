import os
import sys
import json
from pprint import pprint
import csv
from time import sleep
import re

line_width = 80
setup_file = 'filewatcher_config.json'
setup_file_path = os.path.join(os.curdir, setup_file)
file_config = None

def load_json(path_to_file):
    if os.path.isfile(path_to_file):
        with open(path_to_file, 'r') as f:
            return json.load(f)
    else:
        err_msg('kunne ikke finde {0}'.format(path_to_file))

# def save_json(path_to_file):
#     with open(path_to_file, 'w', newline='\n') as f:
#         json.dump(files_dict, f, sort_keys=False, indent=4)
#     print('done')

def load_logfile(path_to_file):
    if os.path.isfile(path_to_file):
        with open(path_to_file, 'r') as f:
            return f.read()
    else:
        err_msg('log mangler, ny oprettet på {0}'.format(path_to_file))
        with open(path_to_file, 'x') as f:
            return load_logfile(path_to_file)

def save_logfile(data, path_to_file):
    if os.path.isfile(path_to_file):
        with open(path_to_file, 'w') as f:
            f.write(data)

def err_msg(my_msg, severe=False):
    space_left = line_width - len(my_msg) - 6
    my_line = '-'*(space_left//2)
    print('\n FEJL: {0} {1} {0}\n'.format(my_line, my_msg))
    if severe:
        sys.exit(1)

def run():

    file_config = load_json(setup_file_path)

    output_file = load_logfile(file_config['output_file'])

    pprint(file_config['output_file'])
    """
    214  "FLYING VICE ALARM - TIME OUT CLAMP 9 OPENING"   6/4/2017   06:48:22
    217  "FLYING VICE ALARM - TIME OUT CLAMP 10 VICE OPENING"   6/4/2017   06:48:22
    214  "FLYING VICE ALARM - TIME OUT CLAMP 9 OPENING"   6/4/2017   08:40:26
    22  "ALARM GRIPPER 1 - Gripper 1 closed when empty"   6/4/2017   15:43:45
    214  "FLYING VICE ALARM - TIME OUT CLAMP 9 OPENING"   6/4/2017   18:53:48
    217  "FLYING VICE ALARM - TIME OUT CLAMP 10 VICE OPENING"   6/4/2017   18:53:48
    """
    for item in file_config['input_files']:
        if os.path.isfile(item):
            tmp_file = load_logfile(item)
            for line in tmp_file:

                code_pattern = r'^[0-9]{3}'
                #desc_pattern = r'([A-Za-z0-9_\./\\-]*)'
                #time_pattern = r'[0-9]{2}:[0-9]{2}:[0-9]{2}'
                #date_pattern = r'([0-9]?[0-9]\/){2}\/[0-9]{4}'
                err_code = re.match(code_pattern, line)
                if err_code:
                    print(type(err_code))
                    pprint(err_code.string)
                #err_desc = re.match(desc_pattern, line)
                #err_date = re.match(date_pattern, line)
                #err_time = re.match(time_pattern, line)
                output_line = '{0}, {1}'.format(item, err_code)
                #output_line = '{0}, {1}, {2}, {3}, {4}'.format(item, err_code, err_desc, err_date, err_time)
                if not output_line in output_file:
                    output_file += '\n{0}'.format(output_line)
            save_logfile(output_file, file_config['output_file'])

        else:
            err_msg('kunne ikke finde {0}'.format(item), severe=False)

if __name__ == '__main__':
    counter = 0
    while True:
        counter += 1
        run()
        print('loop kørt {0} gang(e)'.format(counter))
        sleep(15)
