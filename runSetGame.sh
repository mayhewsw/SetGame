autogain
echo Changing directory to /media/sda1/BeagleSetGame
cd /media/sda1/BeagleSetGame
echo
echo This will run the python Set playing game.
echo This will also kill the matrix gui, and start in a terminal.
echo To quit the game, do Ctrl-C in the terminal that runs it 
echo Or type Enter or Escape in one of the image windows
echo Starting in 5 seconds...



pkill matrix
gnome-terminal -x python runner.py
