package io.github.mayhewsw.setgame;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

import javax.swing.JPanel;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DrawPanel extends JPanel implements MouseListener, MouseMotionListener {

	private Logger logger = LoggerFactory.getLogger(this.getClass());

	/**
	 * 
	 */
	private static final long serialVersionUID = 7760671663802496957L;
	private ArrayList<SetShape> rects;
	private HashSet<SetShape> annotatedRects;
	private SetShape selectedrect = null;

	DrawPanel() {
		// set a preferred size for the custom panel.
		setPreferredSize(new Dimension(640, 480));

		rects = new ArrayList<SetShape>();
		annotatedRects = new HashSet<SetShape>();

		this.addMouseListener(this);
		this.addMouseMotionListener(this);
	}

	@Override
	public void paintComponent(Graphics g) {
		super.paintComponent(g);

		Graphics2D g2 = (Graphics2D) g;
		g2.setStroke(new BasicStroke(2));

		for (SetShape rect : rects) {
			g2.setColor(Color.black);
			if (rect.equals(selectedrect)) {
				g2.setColor(Color.red);
			} else if (annotatedRects.contains(rect)) {
				g2.setColor(Color.green);
			}

			g2.drawRect(rect.x, rect.y, rect.width, rect.height);

		}
	}

	@Override
	public void mouseClicked(MouseEvent arg0) {
		// TODO Auto-generated method stub
	}

	@Override
	public void mouseEntered(MouseEvent arg0) {
		// TODO Auto-generated method stub

	}

	@Override
	public void mouseExited(MouseEvent arg0) {
		// TODO Auto-generated method stub

	}

	public void deleteSelected() {
		if (selectedrect != null) {
			for (int i = 0; i < rects.size(); i++) {
				if (rects.get(i).equals(selectedrect)) {
					rects.remove(i);
					this.repaint();
					return;
				}
			}
		}
	}

	@Override
	public void mousePressed(MouseEvent arg0) {
		System.out.println("creating rect...");
		rects.add(0, new SetShape(arg0.getX(), arg0.getY(), 0, 0));
		this.repaint();

	}

	@Override
	public void mouseReleased(MouseEvent arg0) {
		if (rects.get(0).width < 5 || rects.get(0).height < 5) {
			System.out.println("oh, never mind, too small.");
			rects.remove(0);
			selectedrect = null;
			this.repaint();
		}

		for (SetShape rect : rects) {
			if (rect.contains(arg0.getX(), arg0.getY())) {
				System.out.println("selection happening");
				selectedrect = rect;
				this.repaint();
				return;
			}

		}

		System.out.println(rects);
	}

	@Override
	public void mouseDragged(MouseEvent arg0) {

		SetShape prevrect = rects.remove(0);
		SetShape newone = new SetShape(prevrect.x, prevrect.y, arg0.getX() - prevrect.x, arg0.getY() - prevrect.y);
		rects.add(0, newone);
		selectedrect = newone;
		this.repaint();
	}

	@Override
	public void mouseMoved(MouseEvent arg0) {
		// TODO Auto-generated method stub

	}

	public void clearrects() {
		this.rects.clear();

	}

	public void setRects(ArrayList<SetShape> rects) {
		this.rects = rects;
		this.annotatedRects = new HashSet<>(rects);
	}

	public void saveRects(String fname) {
		System.out.println(fname);

		String datname = fname + ".dat";
		
		// String name = f.getName();
		// String savedir = f.getParent();

		try {
			BufferedWriter b = new BufferedWriter(new FileWriter(datname, false));

			for (SetShape rect : rects) {
				b.write(rect.toString() + "\n");
			}
			b.close();

		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public void saveRectAttrs(String color, String shape, String fill) {
		if (selectedrect != null) {
			System.out.println("OK, saving rect attrs");
			System.out.println(String.format("They are: %s, %s, %s.", color, shape, fill));

			selectedrect.addAttrs(color, shape, fill);

			annotatedRects.add(selectedrect);
			selectedrect = null; // will this invalidate the above line???
			this.repaint();

			System.out.println(annotatedRects);
			// associate selectedrect with the following attributes: color, shape, fill
			// good!
		} else {
			System.out.println("No rect is selected...");
		}
	}

}
