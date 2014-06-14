package io.github.mayhewsw.setgame;

import io.github.mayhewsw.util.SetUtil;

import java.io.FileReader;
import java.io.IOException;
import java.util.List;

import org.apache.commons.io.IOUtils;
import org.opencv.core.Mat;
import org.opencv.highgui.Highgui;

import edu.illinois.cs.cogcomp.lbjava.parse.Parser;


public class DumbThing implements Parser {

	String[] fnames;
	int currimg;
	List<String> currlines = null;
	int currline;

	public DumbThing(String openpath) {
		// this will open images and text files.
		// For each image, a corresponding text file.
		fnames = SetUtil.listFiles(openpath);
		
		for (int i = 0; i < fnames.length; i++) {
			this.fnames[i] = openpath + "/" + fnames[i];
		}
		
		currimg = 0;

	}

	@Override
	public void close() {
		// TODO Auto-generated method stub

	}

	@SuppressWarnings("unchecked")
	@Override
	public Object next() {

		String fname = fnames[currimg];
		if (currlines == null) {
			// load image and data file (if it has a corresponding text file)

			// read lines from file
			try {
				currlines = IOUtils.readLines(new FileReader(fname + ".dat"));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
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

	@Override
	public void reset() {
		// TODO Auto-generated method stub

	}
	
//	public static void main(String[] args){
//		PropertiesConfiguration config;
//		try {
//			config = new PropertiesConfiguration("setgame.conf");
//			System.load(config.getString("libpath"));
//			
//			ImageReader r = new ImageReader(config.getString("savepath"));
//			
//			SetShape ss;
//			ImgFrame f = new ImgFrame("SetGame Viewer");
//			
//			while((ss = (SetShape) r.next()) != null){
//				f.setImg(ss.img, ss.width, ss.height);
//				System.out.println(ss);	
//				System.in.read();
//			}
//			
//		} catch (ConfigurationException c) {
//			c.printStackTrace();
//		} catch (IOException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		} 	
//
//	}

}
