# Harmonic


A UI interface for database that leads with a conversational UI

## TODO:

- make an api interface for the application to use to interact with the server.  This way we don't need to mess with database permissions client side.  All database interaction can happen on server.  strict user verification on all queries

- make utilities for the app to hit against the endpoints defined in routers

- make login screen and connect the success signal to the homepage.


# building application using pyinstaller



`pyinstaller --onefile --windowed --hidden-import=requests --icon=homepage/icons/favicon.ico main.py`

Then edit the spec file to include `Tree('path/to/project')` in the EXE args after pyz

I think that so long as the project doesn't change structure I can make changes to the project itself and then just rebuild from spec file

Need to make sure to delete the build and dist folders before doing so.

THen to create a dmg file use

`pushd dist`
`hdiutil create ./harmonic.dmg -srcfolder harmonic.app -ov`
`popd`