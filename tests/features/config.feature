Feature: Arrangemusic Configuration
	In order to use arrangemusic comfortably
	the user should be able to save a configuration and
	as a lazy programmer, the configuration class should be
	very intelligent, so that throughout the application all
	code regarding configuration options is easy and cute.
	Scenario: Two Configuration objects
		Given I have a fresh Configuration object
		And I have a second Configuration object
		Then both should have the same ID.
	
	Scenario: Configuration defaults
		Given I have a fresh Configuration object 'conf'
		Then "conf.interactive" should be false
		And "conf.pattern" should be internal
		And "conf.dryrun" should be true
		And "conf.verbose" should be false
