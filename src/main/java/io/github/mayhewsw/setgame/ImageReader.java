package io.github.mayhewsw.setgame;

import io.github.mayhewsw.util.SetUtil;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;

import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.PropertiesConfiguration;
import org.apache.commons.io.IOUtils;
import org.opencv.core.Mat;
import org.opencv.highgui.Highgui;

import edu.illinois.cs.cogcomp.lbjava.parse.Parser;


public class ImageReader implements Parser {

	String[] fnames;
	int currimg;
	List<String> currlines = null;
	int currline;

	public ImageReader(String openpath) {
		
		PropertiesConfiguration config;
		try {
			// It needs to be this way, because LBJava doesn't know about classpath...
			config = new PropertiesConfiguration("src/main/resources/setgame.conf");
			//config = new PropertiesConfiguration("setgame.conf");
			System.load(config.getString("libpath"));
			
		} catch (ConfigurationException c) {
			c.printStackTrace();
		} 
		
		if(! new File(openpath).exists()){
			System.out.println("Whoops can't find: " + openpath);
		}
		
		// this will open images and text files.
		// For each image, a corresponding text file.
		fnames = SetUtil.listFiles(openpath);
		
		for (int i = 0; i < fnames.length; i++) {
			this.fnames[i] = openpath + "/" + fnames[i];
		}
		
		if(fnames.length == 0){
			System.out.println("Whoops: no files in this directory?");
		}
	
		
		currimg = 0;

	}

	//@Override
	public void close() {
		// TODO Auto-generated method stub

	}

	@SuppressWarnings("unchecked")
	//@Override
	public Object next() {

		if(currimg >= fnames.length) return null;
		
		String fname = fnames[currimg];
		if (currlines == null) {
			// load image and data file (if it has a corresponding text file)

			// read lines from file
			try {
				currlines = IOUtils.readLines(new FileReader(fname + ".dat"));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				//e.printStackTrace();
				return null; // FIXME: ugly!
			}

			currline = 0;				
		}
		
		Mat img = Highgui.imread(fname);
		SetShape ss = SetShape.fromString(currlines.get(currline++));
		
		ss.setImg(img.submat(ss.y, ss.y + ss.height, ss.x, ss.x + ss.width));
		
		if(currline >= currlines.size()){
			currlines = null;
			currimg++;
		}
		
		return ss;
	}

	//@Override
	public void reset() {
		// TODO Auto-generated method stub

	}
	
	public static void main(String[] args) throws IOException{
		System.out.println("Got nothin");
		
		ImageReader i = new ImageReader("../images/training");

		ImgFrame f = new ImgFrame("Colors");
		
		SetShape ss;
		for(int j = 0; j > -1; j++){
			ss = (SetShape) i.next();
			int[] s = ss.getColorFeatures();
			System.out.println(Arrays.toString(s));
			f.setImg(ss.img);
			System.in.read();

		}
		
		

		

		
		

	}

}
