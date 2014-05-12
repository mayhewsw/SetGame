package io.github.mayhewsw.face;

import io.github.mayhewsw.setgame.ImgFrame;
import io.github.mayhewsw.setgame.SetRunner;

import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.PropertiesConfiguration;
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfRect;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.highgui.VideoCapture;
import org.opencv.objdetect.CascadeClassifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FaceDetect {

	private final int COMPUTER_WEBCAM = 0;
	private final int PSEYE = 1;

	private final int CAMERA_IN_USE = COMPUTER_WEBCAM;

	private CascadeClassifier faceDetector;

	PropertiesConfiguration config = null;

	private Logger logger = LoggerFactory.getLogger(this.getClass());

	public FaceDetect() {
		try {
			config = new PropertiesConfiguration("setgame.conf");
			System.load(config.getString("libpath"));
			faceDetector = new CascadeClassifier("src/main/resources/lbpcascade_frontalface.xml");

		} catch (ConfigurationException c) {
			logger.error("Whoops. Configuration is not working!");
			c.printStackTrace();
		}
	}

	/**
	 * Detects faces in an image, draws boxes around them, and writes the results to
	 * "faceDetection.png".
	 */
	public void run() {
		System.out.println("\nRunning FaceDetect");

		VideoCapture v = new VideoCapture();

		System.out.println(v.open(CAMERA_IN_USE));

		Mat image = new Mat();

		ImgFrame f = new ImgFrame("Face Detector");
		f.saveTo(config.getString("savepath"));

		v.read(image);
		 Rect[] faceDetections = detectFace(image);

		for (int i = 0; i > -1; i++) {
			v.read(image);

			 if (i % 10 == 0) {
			 faceDetections = detectFace(image);
			 }

			// Draw a bounding box around each face.
			if (faceDetections.length > 0) {
				for (Rect rect : faceDetections) {
					Core.rectangle(image, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y + rect.height), new Scalar(0, 255, 0));
				}
			}

			if (ImgFrame.done) {
				break;
			}

			f.setImg(image);

		}

		f.dispose();

		// Highgui.imwrite("webcamcapture.png", image);

	}

	public Rect[] detectFace(Mat image) {
		// Create a face detector from the cascade file in the resources
		// directory.
		// CascadeClassifier faceDetector = new
		// CascadeClassifier(getClass().getResource("/lbpcascade_frontalface.xml").getPath());
		// Mat image = Highgui.imread(getClass().getResource("/stephen.jpg").getPath());

		// Mat image = Highgui.imread("src/main/resources/stephen.jpg");

		// Detect faces in the image.
		// MatOfRect is a special container class for Rect.
		MatOfRect faceDetections = new MatOfRect();
		faceDetector.detectMultiScale(image, faceDetections);

		System.out.println(String.format("Detected %s faces", faceDetections.toArray().length));

		// Draw a bounding box around each face.
		for (Rect rect : faceDetections.toArray()) {
			Core.rectangle(image, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y + rect.height), new Scalar(0, 255, 0));
		}

		// // Save the visualized detection.
		// String filename = "faceDetection.png";
		// System.out.println(String.format("Writing %s", filename));
		// Highgui.imwrite(filename, image);
		return faceDetections.toArray();
	}

	// public static int showResult(Mat img) {
	// return showResult(img, "Untitled");
	// }

	public static void main(String[] args) {
		FaceDetect sr = new FaceDetect();
		sr.run();
	}
}