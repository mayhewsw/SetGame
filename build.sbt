organization := "io.github.mayhewsw"

name := "SetGame"

version := "1.0-SNAPSHOT"

scalaVersion := "2.9.2"

libraryDependencies += "javax.media" % "jmf" % "2.1.1e"

libraryDependencies += "org.apache.commons" % "commons-io" % "1.3.2"

libraryDependencies += "commons-configuration" % "commons-configuration" % "1.6"

libraryDependencies += "org.slf4j" % "slf4j-api" % "1.7.5"

libraryDependencies += "org.slf4j" % "slf4j-simple" % "1.7.5"

EclipseKeys.projectFlavor := EclipseProjectFlavor.Java

EclipseKeys.eclipseOutput := Some("bin")

EclipseKeys.createSrc := EclipseCreateSrc.Default + EclipseCreateSrc.Resource

lazy val makeclasspath = taskKey[Unit]("An example task")

makeclasspath := {
   val p = new java.io.PrintWriter(new java.io.File("cp.txt"))
}

lazy val getLBJSettings = taskKey[Map[String, String]]("Gets LBJ Settings")

getLBJSettings := {
   val dflag = "bin"
   val sourcepath = "src/main/java"
   Map("dflag" -> dflag, "sourcepath" -> sourcepath)
}
   
lazy val lbjcompile = inputKey[Unit]("Compile LBJ stuff")

lbjcompile := {
   import complete.DefaultParsers._
   println("Compiling LBJ...")
   val args: Seq[String] = spaceDelimited("<arg>").parsed
   val lbjsettings: Map[String, String] = getLBJSettings.value
   println(lbjsettings)
   val cp: String = ((dependencyClasspath in Compile).value.files).mkString(":") + ":" + lbjsettings("dflag")
   "java -cp %s LBJ2.Main -d %s -gsp %s -sourcepath %s %s".format(cp, lbjsettings("dflag"), lbjsettings("sourcepath"), lbjsettings("sourcepath"), args.head) !
}

lazy val lbjclean = inputKey[Unit]("Remove LBJ stuff")

lbjclean := {
   import complete.DefaultParsers._
   println("Cleaning LBJ...")
   val args: Seq[String] = spaceDelimited("<arg>").parsed
   println(args)
   val lbjsettings: Map[String, String] = getLBJSettings.value
   val cp: String = ((dependencyClasspath in Compile).value.files).mkString(":") + ":" + lbjsettings("dflag")
   "java -cp %s LBJ2.Main -x -d %s -gsp %s -sourcepath %s %s".format(cp, lbjsettings("dflag"), lbjsettings("sourcepath"), lbjsettings("sourcepath"), args.head) !
}

val demo = inputKey[Unit]("A demo input task.")

demo := {
   import complete.DefaultParsers._
    // get the result of parsing
    val args: Seq[String] = spaceDelimited("<arg>").parsed
    // Here, we also use the value of the `scalaVersion` setting
    println("The current Scala version is " + scalaVersion.value)
    println("The arguments to demo were:")
    args foreach println
 }