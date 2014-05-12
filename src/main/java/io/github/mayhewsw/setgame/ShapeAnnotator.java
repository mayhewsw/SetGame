package io.github.mayhewsw.setgame;

import io.github.mayhewsw.util.SetUtil;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.PropertiesConfiguration;
import org.apache.commons.io.IOUtils;
import org.opencv.highgui.Highgui;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ShapeAnnotator extends ImgFrame {

	/**
	 * 
	 */
	private static final long serialVersionUID = -2822002259728448176L;
	PropertiesConfiguration config = null;
	String[] fnames;

	private Logger logger = LoggerFactory.getLogger(this.getClass());
	public int currImgInd;
	public DrawPanel pan;

	public ShapeAnnotator() {
		super("Annotator Window");

		try {
			config = new PropertiesConfiguration("setgame.conf");
			System.load(config.getString("libpath"));

		} catch (ConfigurationException c) {
			logger.error("Whoops. Configuration is not working!");
			c.printStackTrace();
		}

		String savepath = config.getString("savepath");
		this.fnames = SetUtil.listFiles(savepath);

		for (int i = 0; i < fnames.length; i++) {
			this.fnames[i] = savepath + "/" + fnames[i];
		}

		currImgInd = 0;

		// Container content = this.getContentPane();
		this.add(new ButtonPanel(this));

		pan = new DrawPanel();
		pan.setBounds(0, 0, 640, 480);
		pan.setOpaque(false);

		imglabel.add(pan);

		this.pack();
		this.setVisible(true);

		// this needs to be before the JPanel
		this.nextImg();

	}

	public void nextImg() {
		if (currImgInd >= fnames.length) {
			return;
		}

		String fname = fnames[currImgInd++];
		this.setImg(Highgui.imread(fname));

		pan.clearrects();
		
		
		File datafile = new File(fname + ".dat");
		if (datafile.exists()) {
			try {

				List<String> lines = IOUtils.readLines(new FileReader(datafile));

				ArrayList<SetShape> rects = new ArrayList<SetShape>();

				for (String line : lines) {
					if (line.trim().length() > 0) {
						rects.add(SetShape.fromString(line));
					}
				}
				
				pan.setRects(rects);

			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		} else {
			System.out.println("OK, won't load rectangles then...");
		}


		System.out.println("Now displaying: " + fnames[currImgInd - 1]);

	}

	public static void main(String[] args) {
		ShapeAnnotator s = new ShapeAnnotator();
	}

}
