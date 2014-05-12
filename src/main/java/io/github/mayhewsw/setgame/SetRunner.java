package io.github.mayhewsw.setgame;

import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.PropertiesConfiguration;
import org.opencv.core.Mat;
import org.opencv.highgui.Highgui;
import org.opencv.highgui.VideoCapture;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SetRunner {

	private final int WEBCAM = 0;
	private final int PSEYE = 1;

	PropertiesConfiguration config = null;

	private Logger logger = LoggerFactory.getLogger(this.getClass());

	public SetRunner() {
		try {
			config = new PropertiesConfiguration("setgame.conf");
			System.load(config.getString("libpath"));

		} catch (ConfigurationException c) {
			logger.error("Whoops. Configuration is not working!");
			c.printStackTrace();
		}
	}

	public void run() {
		System.out.println("\nRunning SetGame");

		VideoCapture v = new VideoCapture(1);
		
		v.open(1);
		
		//v.grab();
		// boolean b = v.set(4, 160);
		boolean b = v.set(Highgui.CV_CAP_PROP_FRAME_WIDTH, 1280);
		boolean b2 = v.set(Highgui.CV_CAP_PROP_FRAME_HEIGHT, 800);
		System.out.println(b + " " + b2);

		 //System.out.println(v.get(Highgui.CV_CAP_PROP_FRAME_WIDTH)); //to get the actual width of
		// the camera
		 //System.out.println(v.get(Highgui.CV_CAP_PROP_FRAME_HEIGHT));//to get the actual height of
		// the camera

		// v.set(10, 0);

		//System.out.println(v.getSupportedPreviewSizes());

		// just opens an int
		// v.open(1);

		// System.out.println(v.get(Highgui.CV_CAP_PROP_FRAME_WIDTH));
		// System.out.println(v.get(Highgui.CV_CAP_PROP_FRAME_HEIGHT));

		Mat image = new Mat();

		ImgFrame f = new ImgFrame("SetGame Viewer");
		f.saveTo(config.getString("savepath"));

		v.read(image);	

		// Highgui.imwrite("asimpleimg.png", image);

		System.out.println("Image size: " + image.size());

		for (int i = 0; i > -1; i++) {
			v.read(image);

			if (ImgFrame.done) {
				break;
			}

			f.setImg(image);

		}

		f.dispose();
	}

	public static void main(String[] args) {
		SetRunner sr = new SetRunner();
		sr.run();
	}
}