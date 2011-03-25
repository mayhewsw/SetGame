autogain
echo Changing directory to /media/sda1/BeagleSetGame
cd /media/sda1/BeagleSetGame
echo
echo This will run a script so that you can modify the camera inputs
echo Two images will show. Slide the trackbars until the image looks like the second image.
echo Type enter to save the data, and Esc to exit
echo Starting in 5 seconds...
for i in {1..5}
do
    echo -n . 
done

#pkill matrix
gnome-terminal -x python trackBarTest.py
