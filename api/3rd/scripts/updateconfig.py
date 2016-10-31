#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import yaml


def main():
    print len(sys.argv)
    if len(sys.argv) != 12:
        print 'updateconfig.py mysql_host mysql_port mysql_user mysql_pass session_redis_host session_redis_port api_domain session_redis_password'
        sys.exit()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.dirname(base_dir)
    config_file = os.path.join(base_dir, 'config.yaml')
    with open(config_file) as f:
        config = yaml.load(f.read())
    config['general']['debug'] = False
    config['static']['root'] = '/tmp/static/'
    config['log']['filepath'] = '/var/log/pro/pro.log'
    config['database']['name'] = 'drf_project'
    config['database']['host'] = sys.argv[1]
    config['database']['port'] = int(sys.argv[2])
    config['database']['user'] = sys.argv[3]
    config['database']['password'] = sys.argv[4]
    config['session']['host'] = sys.argv[5]
    config['session']['port'] = sys.argv[6]
    config['cloud_api']['domain'] = sys.argv[7]
    config['session']['password'] = sys.argv[8]
    config['cache']['host'] = sys.argv[9]
    config['cache']['port'] = sys.argv[10]
    config['cache']['password'] = sys.argv[11]
    with open(config_file, 'w') as f:
        f.write(yaml.dump(config, default_flow_style=False))


if __name__ == '__main__':
    main()
