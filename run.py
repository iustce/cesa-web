# -*- coding: utf-8 -*-

# python imports
import os
import subprocess
import sys, traceback
try:
	import argparse
except:
	print 'error: please install argparse (sudo pip install argparse)'
	exit(0)


fwpath = os.path.abspath(os.path.dirname(__file__))
venv_dir = os.path.join(fwpath, 'venv')



def get_parser():
	parser = argparse.ArgumentParser(description='Project')
	# Add arguments
	parser.add_argument(
			'-r', '--run', help='run server', required=False, action='store_true')
	parser.add_argument(
			'-co', '--config-object', help='configure from object', metavar='CONFIG_OBJECT', dest='conf_obj', required=False, type=str, nargs=1)
	parser.add_argument(
			'-cf', '--config-file', help='import local config file', metavar='CONFIG_FILE', dest='conf_file', required=False, type=str, nargs=1)
	parser.add_argument(
			'-u', '--update', help='update requirements', required=False, action='store_true')
	return parser


def run():
	app.run(host='0.0.0.0', port=5000)

def develop():
	configure_app(app, DevelopmentConfig())

def product():
	configure_app(app, ProductionConfig())


def import_local_config_file(filename):
	if not os.path.isabs(filename):
		filename = os.path.join(os.getcwd(), filename)
	configure_app(app, filename, is_pyfile=True)


def test():
	pass


def update_requirements():
	subprocess.call([os.path.join(venv_dir, 'bin/pip'), 'install', '-r', os.path.join(fwpath, 'requirements')])



if __name__ == '__main__':
	parser = get_parser()
	args = parser.parse_args()

	if args.update:
		update_requirements()

	elif args.run:
		# project imports
		try:
			from project import app
			from project.application import configure_app
			from project.config import DefaultConfig, DevelopmentConfig, ProductionConfig
		except ImportError:
			print ' *** please install/update requirements or fix the problem ***'
			traceback.print_exc(file=sys.stdout)
			exit(0)

		if args.conf_obj:
			conf_obj = args.conf_obj[0]
			if conf_obj == 'develop':
				develop()
			elif conf_obj == 'product':
				product()
			else:
				print "error: undefined config '%s'" % conf_obj
				exit(0)

		if args.conf_file:
			import_local_config_file(args.conf_file[0])

		run()

	else:
		parser.print_help()

