package io.github.mayhewsw.setgame;

import java.awt.Rectangle;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.Scalar;
import org.opencv.imgproc.Imgproc;

public class SetShape extends Rectangle {

	/**
	 * 
	 */
	private static final long serialVersionUID = 5568143674053201024L;

	String color = null;
	String shape = null;
	String fill = null;

	public Mat img = null;

	public SetShape(int x, int y, int w, int h) {
		super(x, y, w, h);
	}

	public void addAttrs(String color2, String shape2, String fill2) {
		// TODO Auto-generated method stub
		this.color = color2;
		this.shape = shape2;
		this.fill = fill2;
	}

	@Override
	public String toString() {
		return String.format("x=%d y=%d w=%d h=%d shape=%s fill=%s color=%s", this.x, this.y, this.width, this.height, this.shape, this.fill, this.color);
	}

	public static SetShape fromString(String s) {
		String[] parts = s.split("\\s");
		Map<String, String> m = new HashMap<String, String>();

		for (String p : parts) {
			String[] p2 = p.split("=");
			m.put(p2[0], p2[1]);
		}

		int x = Integer.parseInt(m.get("x"));
		int y = Integer.parseInt(m.get("y"));
		int w = Integer.parseInt(m.get("w"));
		int h = Integer.parseInt(m.get("h"));

		SetShape ss = new SetShape(x, y, w, h);
		ss.addAttrs(m.get("color"), m.get("shape"), m.get("fill"));
		return ss;
	}

	public void setImg(Mat submat) {
		this.img = submat;
	}

	public String getColor() {
		return this.color.toLowerCase();
	}

	public String getFill() {
		return this.fill.toLowerCase();
	}

	public String getShape() {
		return this.shape.toLowerCase();
	}

	public double feat() {
		return new Random().nextDouble();
	}

	public String getFillFeatures() {
		// Get all corners
		// Remove all pixels that look like the corners...

		// convert to black and white
		Mat fimg = this.img.clone();
		Imgproc.cvtColor(img, fimg, Imgproc.COLOR_RGB2GRAY);

		ImgFrame i = new ImgFrame("My Title");
		i.setImg(fimg);

		int blocks_horiz = 10;
		int blocks_vert = 10;

		int blockwidth = this.img.width() / blocks_horiz;
		int blockheight = this.img.height() / blocks_vert;

		List<java.lang.Double> l = new ArrayList<>();
		
		// get blocks of image, and get sum of each block
		for (int col = 0; col < this.img.width(); col += blockwidth) {
			for (int row = 0; row < this.img.height(); row += blockheight) {
				Mat sub = fimg.submat(row, row + blockheight, col, col + blockheight);
				double[] v = Core.sumElems(sub).val;
				l.add(v[0]);
			}
		}
		System.out.println(l);
		

		return "FILLLL";
	}

	/**
	 * this is a feature: get the sum of each pixel in the three different channels get the max of
	 * these three sums
	 * 
	 * @return
	 */
	public int[] getColorFeatures() {

		Mat fimg = this.img.clone();

		// List<Mat> chans = new ArrayList<>();
		//
		// for (int i = 0; i < 3; i++) {
		// // NOTE: can use img.type() here, except I want 1 channel, not 3.
		// chans.add(new Mat(this.img.size(), CvType.CV_8UC1));
		// }

		// split into channels...
		// Core.split(fimg, chans);

		Scalar s = Core.sumElems(fimg);
		double[] v = s.val;
		int[] out = new int[3];

		double sum = v[0] + v[1] + v[2];
		for (int i = 0; i < 3; i++) {
			// double divby = Math.pow(10, Math.floor(Math.log10(v[i]))-1);
			out[i] = (int) Math.round(10 * v[i] / sum);

		}
		return out;
	}

}
