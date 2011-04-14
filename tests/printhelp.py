from ArrangeMusic import configuration, tools
import sys

if __name__ == '__main__':
	if len(sys.argv) < 2:
		configuration.CmdlineParser().help()
	else:
		argv = sys.argv[1:]
		configuration.CmdlineParser().parse(argv)
		tools.print_overview()
