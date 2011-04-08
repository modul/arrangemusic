Feature: Commandline Parser
	In order to process commandline options
	arrangemusic must have a commandline parser.

	Scenario: Calling with no arguments
		Given I have my commandline parser object created
		When I let it parse an empty argument list
		Then a configuration instance will hold default options

	Scenario: Calling with no arguments after a configuration was made
		Given I have my commandline parser object created after changing configuration options
		When I let it parse an empty argument list
		Then the configuration should not be altered

	Scenario Outline: Calling with a bunch of arguments
		Given I have my commandline parser object created
		When I let it parse <args>
		Then I will have the options <dryrun>, <verbose>, <interactive>, <target_dir>, <move> set or unset
		
		Examples:
			|    args    | dryrun | verbose | interactive | target_dir |  move |
			| -d         |  False |  False  |   False     |   ./       | False |
			| -nvi       |  True  |  True   |   True      |   ./       | False |
			| -q -t /tmp |  True  |  False  |   True      |   /tmp     | False |
			| -d -I      |  False |  False  |   False     |   /tmp     | False |
			| -m         |  False |  False  |   False     |   /tmp     | True  |
			| -cn        |  True  |  False  |   False     |   /tmp     | False |
			
