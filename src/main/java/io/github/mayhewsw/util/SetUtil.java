package io.github.mayhewsw.util;

import java.io.File;
import java.io.FilenameFilter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Enumeration;
import java.util.List;

import javax.swing.AbstractButton;
import javax.swing.ButtonGroup;

public class SetUtil {

	public enum Color {
		RED, GREEN, PURPLE
	};

	public enum Fill {
		EMPTY, SHADED, FILLED
	};

	public enum Shape {
		SQUIGGLE, OVAL, DIAMOND
	};

	/**
	 * Images are named as: img_XXX.png where XXX are numbers. This extracts the number.
	 * @param f
	 * @return
	 */
	public static Integer getNumName(String f){
		return Integer.parseInt(f.split("\\.")[0].split("_")[1]);
			
	}
	
	public static List<Double> normalize(ArrayList<Double> l){
		double sum = 0;
		for(Double d : l){
			sum += d;
		}
		for (int i = 0; i < l.size(); i++){
			
		}

		
		
		return l;
	}
	
	/**
	 * Get a list of files in a directory, with filename pattern: img*.png
	 * 
	 * @param savepath
	 * @return
	 */
	public static String[] listFiles(String savepath) {
		File d = new File(savepath);

		// Get a list of files, filtered by name
		String[] fnames = d.list(new FilenameFilter() {

			@Override
			public boolean accept(File arg0, String arg1) {
				return arg1.startsWith("img") && arg1.endsWith(".png");
			}
		});

		// Images have the name: img_XX.png. This sorts names by the number XX
		Arrays.sort(fnames, new Comparator<String>() {
			
			public int compare(String f1, String f2) {
				return getNumName(f1).compareTo(getNumName(f2));
			}
		});

		return fnames;
	}

	public static String getSelectedButtonText(ButtonGroup buttonGroup) {
		for (Enumeration<AbstractButton> buttons = buttonGroup.getElements(); buttons.hasMoreElements();) {
			AbstractButton button = buttons.nextElement();

			if (button.isSelected()) {
				return button.getText();
			}
		}

		return null;
	}
}
