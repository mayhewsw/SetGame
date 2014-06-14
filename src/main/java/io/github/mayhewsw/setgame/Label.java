// Modifying this comment will cause the next execution of LBJ2 to overwrite this file.
// F1B88000000000000000B49CC2E4E2A4D294DA65A2A4D4152D1505A282D2A28C94501B2DB825353F49A651C721392537432835B4283321B02551A85351C64751AA5108ABA4B82F41A85F2D35B4C93F372FB84343DA51A61020769E7D05000000

package io.github.mayhewsw.setgame;

import LBJ2.classify.*;
import LBJ2.infer.*;
import LBJ2.learn.*;
import LBJ2.parse.*;


public class Label extends Classifier
{
  public Label()
  {
    containingPackage = "io.github.mayhewsw.setgame";
    name = "Label";
  }

  public String getInputType() { return "io.github.mayhewsw.setgame.SetShape"; }
  public String getOutputType() { return "discrete"; }

  private static String[] __allowableValues = new String[]{ "red", "purple", "green" };
  public static String[] getAllowableValues() { return __allowableValues; }
  public String[] allowableValues() { return __allowableValues; }


  public FeatureVector classify(Object __example)
  {
    return new FeatureVector(featureValue(__example));
  }

  public Feature featureValue(Object __example)
  {
    String result = discreteValue(__example);
    return new DiscretePrimitiveStringFeature(containingPackage, name, "", result, valueIndexOf(result), (short) allowableValues().length);
  }

  public String discreteValue(Object __example)
  {
    if (!(__example instanceof SetShape))
    {
      String type = __example == null ? "null" : __example.getClass().getName();
      System.err.println("Classifier 'Label(SetShape)' defined on line 16 of ColorClassifier.lbj received '" + type + "' as input.");
      new Exception().printStackTrace();
      System.exit(1);
    }

    String __cachedValue = _discreteValue(__example);

    if (valueIndexOf(__cachedValue) == -1)
    {
      System.err.println("Classifier 'Label' defined on line 16 of ColorClassifier.lbj produced '" + __cachedValue  + "' as a feature value, which is not allowable.");
      System.exit(1);
    }

    return __cachedValue;
  }

  private String _discreteValue(Object __example)
  {
    SetShape s = (SetShape) __example;

    return "" + (s.getColor());
  }

  public FeatureVector[] classify(Object[] examples)
  {
    if (!(examples instanceof SetShape[]))
    {
      String type = examples == null ? "null" : examples.getClass().getName();
      System.err.println("Classifier 'Label(SetShape)' defined on line 16 of ColorClassifier.lbj received '" + type + "' as input.");
      new Exception().printStackTrace();
      System.exit(1);
    }

    return super.classify(examples);
  }

  public int hashCode() { return "Label".hashCode(); }
  public boolean equals(Object o) { return o instanceof Label; }
}

