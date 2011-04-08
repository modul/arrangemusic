Feature: Arranger
	In order to rename and move music files
	I wrote the class Arranger to process the file's information
	And construct a new file path based on configuration
	And move or copy the file to it's new place

	Scenario: Generating Paths
		Given I have the configuration from "test.cfg"
		And I have a file "<file>"
		And I have a tag like:
			| key    | value    |
			| artist | <artist> |
			| album  | <album>  |
			| title  | <title>  |
			| year   | <year>   |
			| track  | <track>  |
			| genre  | <genre>  |
		When I load Arranger with it
		Then it should construct "<path>"
			
		Examples:
			|  file       |     artist     |     album     |     title     | year | track |   genre  |path|
			|  file1.mp3  |  Bad Religion  |  No Substance |   Fa fa fa    | 1998 |   6   |   Rock   |B/Bad_Religion/1998-No_Substance/06.Fa_Fa_Fa.mp3|
			|  file1.wma  |  Bad Religion  |  No Substance |   Fa fa fa    | 1998 |   6   |   Rock   | None |
			
	
