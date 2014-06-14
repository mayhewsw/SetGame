
OCVJAR=lib/opencv-300.jar
VERSION=3.0.0

mvn install:install-file -Dfile=$OCVJAR -DgroupId=org.opencv -DartifactId=opencv -Dversion=$VERSION -Dpackaging=jar
