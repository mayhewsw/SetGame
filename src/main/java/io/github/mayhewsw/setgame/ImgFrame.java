package io.github.mayhewsw.setgame;

import io.github.mayhewsw.util.SetUtil;

import java.awt.Component;
import java.awt.Container;
import java.awt.FlowLayout;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Paths;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

import org.apache.commons.io.FilenameUtils;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.core.Size;
import org.opencv.highgui.Highgui;
import org.opencv.imgproc.Imgproc;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ImgFrame extends JFrame {

	private Logger logger = LoggerFactory.getLogger(this.getClass());

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	public static boolean done = false;
	public Mat currimg;

	public int currname = -1;

	private String savepath;

	public JLabel imglabel;

	public ImgFrame(String title) {
		this.setTitle(title + " (Press enter to exit)");

		Container content = this.getContentPane();
		content.setLayout(new FlowLayout());
		
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		this.addKeyListener(new KeyListener() {

			public void keyPressed(KeyEvent e) {
			}

			public void keyReleased(KeyEvent e) {
				if (e.getKeyCode() == KeyEvent.VK_ENTER) {
					System.out.println("You pressed enter!");
					System.out.println("Exiting now");
					ImgFrame.done = true;

				} else if (e.getKeyCode() == KeyEvent.VK_SPACE) {
					// save img
					saveImg();
				}
			}

			public void keyTyped(KeyEvent e) {
			}
		});

		imglabel = new JLabel();
		this.getContentPane().add(imglabel);
		
		this.pack();
		this.setVisible(true);
				
	}

	public void saveTo(String path) {
		this.savepath = path;
	}

	public void saveImg() {
		if (currname == -1) {

			String[] fnames = SetUtil.listFiles(this.savepath);

			int max = 0;

			// If there are no files, let's start with number 1!
			if (fnames.length == 0) {
				currname = 0; // it increments first... so 0 becomes 1
			} else { // get the largest named file in the directory
				for (String name : fnames) {
					logger.debug(FilenameUtils.removeExtension(name));
					int n = Integer.parseInt(FilenameUtils.removeExtension(name).split("_")[1]);
					if (n > max) {
						max = n;
					}
				}
				currname = max;
			}
		}

		String name = Paths.get(this.savepath).resolve("img_" + ++currname + ".png").toString();
		System.out.println("Writing image to:" + name);
		Highgui.imwrite(name, this.currimg);
	}
	
	public void setImg(Mat img){
		setImg(img, 1280, 984);
	}

	public void setImg(Mat img, int w, int h) {

		this.currimg = img;

		//Imgproc.resize(img, img, new Size(w,h));
		MatOfByte matOfByte = new MatOfByte();
		Highgui.imencode(".jpg", img, matOfByte);
		byte[] byteArray = matOfByte.toArray();
		BufferedImage bufImage = null;

		InputStream in = new ByteArrayInputStream(byteArray);
		try {
			bufImage = ImageIO.read(in);
		
			imglabel.setIcon(new ImageIcon(bufImage));
			imglabel.updateUI();
			this.pack();
			
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
