#! `which python3`
"""Helper script for deployment."""

import argparse
import subprocess

parser = argparse.ArgumentParser(
    description='Aides-territoires deployment script')

parser.add_argument(
    'deployment_type',
    choices=['full', 'build'],
    help='Run full deployment or only build subset')
parser.add_argument(
    '-e',
    '--env',
    nargs='+',
    dest='envs',
    choices=['local', 'stage', 'prod'],
    default=['local'],
    help='List of hosts to deploy to')


def deploy():
    args = parser.parse_args()
    envs = ','.join(args.envs)

    if 'prod' in args.envs:
        print('Warning! You are about to deploy in production!')
        res = input('Are you sure you want to proceed? [y/N] ')
        if res != 'y':
            return

    deployment_args = [
        './ansible-playbook-dotenv.sh',
        '-i',
        './deployment/hosts',
        './deployment/site.yml',
        '-l',
        envs,
    ]

    if args.deployment_type == 'build':
        deployment_args += ['--start-at-task=Build']

    print('Running command:')
    print(' '.join(deployment_args))
    subprocess.run(deployment_args)


if __name__ == '__main__':
    deploy()
