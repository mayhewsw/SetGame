package io.github.mayhewsw.setgame;

import io.github.mayhewsw.util.SetUtil;

import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.JRadioButton;

public class ButtonPanel extends JPanel {

	public ButtonPanel(final ShapeAnnotator s) {

		this.setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));

		JButton nxtBtn = new JButton("Next");
		nxtBtn.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				String fname = s.fnames[s.currImgInd - 1];
				System.out.println("saving rects to: " + fname);
				s.pan.saveRects(fname);
				s.nextImg();
			}

		});
		this.add(nxtBtn);
		this.add(Box.createRigidArea(new Dimension(0, 10)));
		
		JButton saveBtn = new JButton("Save Rects...");
		saveBtn.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent arg0) {
				String fname = s.fnames[s.currImgInd - 1];
				System.out.println("saving rects to: " + fname);
				s.pan.saveRects(fname);

			}
		});
		this.add(saveBtn);

		JButton delBtn = new JButton("Delete Rect");
		delBtn.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				System.out.println("delete something");
				s.pan.deleteSelected();

			}

		});
		this.add(delBtn);

		// /////////////////////////////////////////////
		// Color radio buttons
		// /////////////////////////////////////////////
		JRadioButton redButton = new JRadioButton("Red");
		redButton.setMnemonic(KeyEvent.VK_R);
		redButton.setSelected(true);

		JRadioButton greenButton = new JRadioButton("Green");
		greenButton.setMnemonic(KeyEvent.VK_G);

		JRadioButton purpleButton = new JRadioButton("Purple");
		purpleButton.setMnemonic(KeyEvent.VK_P);
		// Group the radio buttons.
		final ButtonGroup colorgroup = new ButtonGroup();
		colorgroup.add(redButton);
		colorgroup.add(greenButton);
		colorgroup.add(purpleButton);
		this.add(redButton);
		this.add(greenButton);
		this.add(purpleButton);
		this.add(Box.createRigidArea(new Dimension(0, 10)));

		// /////////////////////////////////////////////
		// Fill radio buttons
		// /////////////////////////////////////////////
		// Set mnemonics
		JRadioButton emptyButton = new JRadioButton("Empty");
		emptyButton.setMnemonic(KeyEvent.VK_E);
		emptyButton.setSelected(true);

		JRadioButton shadedButton = new JRadioButton("Shaded");
		shadedButton.setMnemonic(KeyEvent.VK_H);

		JRadioButton filledButton = new JRadioButton("Filled");
		filledButton.setMnemonic(KeyEvent.VK_F);

		// Group the radio buttons.
		final ButtonGroup fillgroup = new ButtonGroup();
		fillgroup.add(emptyButton);
		fillgroup.add(shadedButton);
		fillgroup.add(filledButton);

		this.add(emptyButton);
		this.add(shadedButton);
		this.add(filledButton);
		this.add(Box.createRigidArea(new Dimension(0, 10)));

		// /////////////////////////////////////////////
		// Shape radio buttons
		// /////////////////////////////////////////////
		JRadioButton squiggleButton = new JRadioButton("Squiggle");
		squiggleButton.setMnemonic(KeyEvent.VK_S);
		squiggleButton.setSelected(true);

		JRadioButton diamondButton = new JRadioButton("Diamond");
		diamondButton.setMnemonic(KeyEvent.VK_D);

		JRadioButton ovalButton = new JRadioButton("Oval");
		ovalButton.setMnemonic(KeyEvent.VK_O);

		// Group the radio buttons.
		final ButtonGroup shapegroup = new ButtonGroup();
		shapegroup.add(squiggleButton);
		shapegroup.add(diamondButton);
		shapegroup.add(ovalButton);

		this.add(squiggleButton);
		this.add(diamondButton);
		this.add(ovalButton);
		this.add(Box.createRigidArea(new Dimension(0, 10)));

		JButton saveRectBtn = new JButton("Save Rect");
		saveRectBtn.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				s.pan.saveRectAttrs(SetUtil.getSelectedButtonText(colorgroup), SetUtil.getSelectedButtonText(shapegroup), SetUtil.getSelectedButtonText(fillgroup));
			}

		});
		saveRectBtn.setMnemonic(KeyEvent.VK_S);
		this.add(saveRectBtn);

		JButton exitBtn = new JButton("Exit");
		exitBtn.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent arg0) {
				System.exit(1);
			}

		});
		this.add(Box.createRigidArea(new Dimension(0, 20)));
		this.add(exitBtn);
	}

}
