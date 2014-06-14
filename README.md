## SetGame

Written in Java, using LBJava. 

To Run this project, open eclipse. SetRunner.java is the one you want.

You can also run:

>> sbt "lbjclean src/main/lbj/FillClassifier.lbj"
>> sbt "lbjcompile src/main/lbj/FillClassifier.lbj"
>> sbt run

To generate the eclipse files for the project, run

>> sbt eclipse

But this is not complete. The .classpath file will need some
editing. This just takes everything from the lib folder and puts it on
the classpath. If there are files in the lib folder that are not jars
(the .so file, for example), then these should be removed from the
build path in Eclipse. Next, for the opencv jar, include the folder
that contains the libopencv_javaXXX.so file as the Native Library
Location (Build Path, Libraries tab).
