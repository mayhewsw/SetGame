package io.github.mayhewsw.util;

import io.github.mayhewsw.setgame.ImageReader;
import io.github.mayhewsw.setgame.SetShape;

public class SandBox {

	public static void main(String[] args) {

		ImageReader i = new ImageReader("../images/training");
		SetShape s = null;
		for (int j = 0; j < 35; j++){
			s = (SetShape) i.next();
		}
		System.out.println(s.getFillFeatures());

	}

}
