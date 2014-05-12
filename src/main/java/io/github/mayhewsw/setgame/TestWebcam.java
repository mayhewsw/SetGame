package io.github.mayhewsw.setgame;
//package io.github.mayhewsw.facetest;
//
//import java.awt.BorderLayout;
//import java.awt.FlowLayout;
//import java.awt.Graphics;
//import java.awt.event.ActionEvent;
//import java.awt.event.ActionListener;
//import java.awt.image.BufferedImage;
//import java.util.Timer;
//import java.util.TimerTask;
//
//import javax.swing.JButton;
//import javax.swing.JFrame;
//import javax.swing.JPanel;
//
//public class TestWebcam extends JFrame {
//	  private FrameGrabber vision;
//	  private BufferedImage image;
//	  private VideoPanel videoPanel = new VideoPanel();
//	  private JButton jbtCapture = new JButton("Show Video");
//	  private Timer timer = new Timer();
//
//	  public TestWebcam() {
//	    JPanel jpButton = new JPanel();
//	    jpButton.setLayout(new FlowLayout());
//	    jpButton.add(jbtCapture);
//
//	    setLayout(new BorderLayout());
//	    add(videoPanel, BorderLayout.CENTER);
//	    add(jpButton, BorderLayout.SOUTH);
//	    setVisible(true);
//
//	    jbtCapture.addActionListener(
//	       new ActionListener() {
//	          public void actionPerformed(ActionEvent e) {
//	               timer.schedule(new ImageTimerTask(), 1000, 33);
//	          }
//	       }
//	   );
//	  }
//
//	  class ImageTimerTask extends TimerTask {
//	     public void run() {  
//	         videoPanel.showImage();
//	     }
//	  }
//
//	  class VideoPanel extends JPanel {
//	      public VideoPanel() {
//	        try {
//	    		vision = new FrameGrabber();
//	    		vision.start();
//	    	} catch (FrameGrabberException fge) {
//	    	}
//	      }
//
//	      protected void paintComponent(Graphics g) {
//	        super.paintComponent(g);
//	        if (image != null)
//	           g.drawImage(image, 10, 10, 160, 120, null);
//	      }
//
//	      public void showImage() {
//	    	  image = vision.getBufferedImage();
//	    	  repaint();   
//	      }
//	  }
//
//	  public static void main(String[] args) {
//	        TestWebcam frame = new TestWebcam();
//	        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
//	        frame.setSize(190, 210);
//	        frame.setVisible(true);
//	  }
//	}