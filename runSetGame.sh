autogain
echo Changing directory to /media/sda1/BeagleSetGame
cd /media/sda1/BeagleSetGame
echo
echo This will run the python Set playing game.
echo This will also kill the matrix gui, and start in a terminal.
echo To quit the game, do Ctrl-C in the terminal that runs it.
echo Starting in 5 seconds...
for i in {1..5}
do
    echo . -n
done


pkill matrix
gnome-terminal -x python runner.py
