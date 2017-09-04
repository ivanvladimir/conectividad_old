// author: @mattgarciablitz - Matias Fernando Garcia-Constantino
// SERG-Ulster University
//
// modified: @Penserbjorne - Sebastian Aguilar
// FI-IIMAS-IIJ-UNAM

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;

import javax.xml.parsers.DocumentBuilderFactory;

import org.apache.commons.io.FilenameUtils;

import gate.Annotation;
import gate.AnnotationSet;
import gate.Corpus;
import gate.CorpusController;
import gate.Document;
import gate.Factory;
import gate.FeatureMap;
import gate.Gate;
import gate.LanguageAnalyser;
import gate.Utils;
import gate.creole.SerialAnalyserController;
import gate.gui.MainFrame;
import gate.util.ExtensionFileFilter;
import gate.util.InvalidOffsetException;
import gate.util.persistence.PersistenceManager;

public class GateEmbedded{

	static String DataFolder = "./../../src/python/data/";

	public static void main(String[] args) throws Exception{

		System.out.println("Prepare the library.");
		Gate.init();

		//System.out.println("Show the main window.");
		//MainFrame.getInstance().setVisible(true);

		System.out.println("Load required plugins.");
		System.out.println("Get the root plugins dir.");
		File pluginsDir = Gate.getPluginsHome();

		System.out.println("Load saved GATE app.");
		CorpusController controller = (CorpusController)PersistenceManager.loadObjectFromFile(new File("./../appgate.gapp"));

		/*
		// Load the "ANNIE" plugin.
		File aPluginDir = new File(pluginsDir, "ANNIE");
		Gate.getCreoleRegister().registerDirectories(aPluginDir.toURI().toURL());
		*/

		System.out.println("Read a corpus.");
		Corpus corpus = Factory.newCorpus("Corpus");

		File directory = new File(DataFolder + "extract_text/"); // TXT

		URL url = directory.toURI().toURL();

		ExtensionFileFilter txtFilter = new ExtensionFileFilter("TXT files", "txt");

		corpus.populate(url, txtFilter, "UTF-8", false);

		/*
		//// Create pipeline to annotate documents in corpus with JAPE rules.
		// Create serialAnalyzerController.
		SerialAnalyserController controller = (SerialAnalyserController)Factory.createResource("gate.creole.SerialAnalyserController");

		// Load Processing Resources.
		LanguageAnalyser documentResetPR = (LanguageAnalyser)Factory.createResource("gate.creole.annotdelete.AnnotationDeletePR", Utils.featureMap("setsToRemove", "Original markups"));
		LanguageAnalyser ANNIE_EnglishTokeniser = (LanguageAnalyser)Factory.createResource("gate.creole.tokeniser.DefaultTokeniser");
		LanguageAnalyser ANNIE_Gazetteer = (LanguageAnalyser)Factory.createResource("gate.creole.gazetteer.DefaultGazetteer");
		LanguageAnalyser ANNIE_SentenceSplitter = (LanguageAnalyser)Factory.createResource("gate.creole.splitter.SentenceSplitter");
		LanguageAnalyser ANNIE_POStagger = (LanguageAnalyser)Factory.createResource("gate.creole.POSTagger");
		LanguageAnalyser ANNIE_NEtransducer = (LanguageAnalyser)Factory.createResource("gate.creole.ANNIETransducer");
		// LanguageAnalyser ANNIE_OrthoMatcher = (LanguageAnalyser)Factory.createResource("gate.creole.orthomatcher.OrthoMatcher");

		// Load JAPE grammar rules.

		// JAPE rules for Document Structure.
		LanguageAnalyser JAPE_LiteralIndex = (LanguageAnalyser)Factory.createResource("gate.creole.Transducer", Utils.featureMap("grammarURL", new File("./../JAPE/LiteralIndex.jape").toURI().toURL(), "encoding", "UTF-8"));
		LanguageAnalyser JAPE_NumericalIndex = (LanguageAnalyser)Factory.createResource("gate.creole.Transducer", Utils.featureMap("grammarURL", new File("./../JAPE/NumericalIndex.jape").toURI().toURL(), "encoding", "UTF-8"));
		LanguageAnalyser JAPE_RomanNumeralIndex = (LanguageAnalyser)Factory.createResource("gate.creole.Transducer", Utils.featureMap("grammarURL", new File("./../JAPE/RomanNumeralIndex.jape").toURI().toURL(), "encoding", "UTF-8"));

		LanguageAnalyser JAPE_PreambleSection = (LanguageAnalyser)Factory.createResource("gate.creole.Transducer", Utils.featureMap("grammarURL", new File("./../JAPE/PreambleSection.jape").toURI().toURL(), "encoding", "UTF-8"));
		LanguageAnalyser JAPE_SubsectionStart = (LanguageAnalyser)Factory.createResource("gate.creole.Transducer", Utils.featureMap("grammarURL", new File("./../JAPE/SubsectionStart.jape").toURI().toURL(), "encoding", "UTF-8"));
		LanguageAnalyser JAPE_Subsection = (LanguageAnalyser)Factory.createResource("gate.creole.Transducer", Utils.featureMap("grammarURL", new File("./../JAPE/Subsection.jape").toURI().toURL(), "encoding", "UTF-8"));
		LanguageAnalyser JAPE_SectionStart = (LanguageAnalyser)Factory.createResource("gate.creole.Transducer", Utils.featureMap("grammarURL", new File("./../JAPE/SectionStart.jape").toURI().toURL(), "encoding", "UTF-8"));
		LanguageAnalyser JAPE_Section = (LanguageAnalyser)Factory.createResource("gate.creole.Transducer", Utils.featureMap("grammarURL", new File("./../JAPE/Section.jape").toURI().toURL(), "encoding", "UTF-8"));
		LanguageAnalyser JAPE_LastSection = (LanguageAnalyser)Factory.createResource("gate.creole.Transducer", Utils.featureMap("grammarURL", new File("./../JAPE/LastSection.jape").toURI().toURL(), "encoding", "UTF-8"));

		controller.add(documentResetPR);
		controller.add(ANNIE_EnglishTokeniser);
		controller.add(ANNIE_Gazetteer);
		controller.add(ANNIE_SentenceSplitter);
		controller.add(ANNIE_POStagger);
		controller.add(ANNIE_NEtransducer);
		// controller.add(ANNIE_OrthoMatcher);

		controller.add(JAPE_LiteralIndex);
		controller.add(JAPE_NumericalIndex);
		controller.add(JAPE_RomanNumeralIndex);

		controller.add(JAPE_PreambleSection);
		controller.add(JAPE_SubsectionStart);
		controller.add(JAPE_Subsection);
		controller.add(JAPE_SectionStart);
		controller.add(JAPE_Section);
		controller.add(JAPE_LastSection);
		*/
		controller.setCorpus(corpus); // Set corpus.
		System.out.println("Execute the corpus.");
		controller.execute(); // Execute the corpus.

		System.out.println("Save annotated documents in corpus to a folder.");
		Set<String> annotTypesRequired = new HashSet<String>();

		System.out.println("AnnotTypesRequired.");
		// Matt Anottations
		annotTypesRequired.add("LiteralIndex");
		annotTypesRequired.add("NumericalIndex");
		annotTypesRequired.add("RomanNumeralIndex");

		annotTypesRequired.add("LastSection");
		annotTypesRequired.add("PreambleSection");
		annotTypesRequired.add("Subsection");
		annotTypesRequired.add("Section");

		// Penserbjorne Anottations
		annotTypesRequired.add("Case");
		annotTypesRequired.add("Date2");
		annotTypesRequired.add("DateSentence");
		annotTypesRequired.add("Actions");
		annotTypesRequired.add("CourtMembers");
		annotTypesRequired.add("PersonCourtMembers");
		annotTypesRequired.add("Articles");
		annotTypesRequired.add("ResolutivePoints");
		annotTypesRequired.add("ConcurrentVote");


		Writer output = null;

		System.out.println("Retrieving documents and their annotations.");
		for(int i = 0; i < controller.getCorpus().size(); i++){

			// Retrieving documents and their annotations.
			AnnotationSet defaultAnnotSet = controller.getCorpus().get(i).getAnnotations();

			Set<Annotation> annotationsRequired = new HashSet<Annotation>(defaultAnnotSet.get(annotTypesRequired));

			File outputTestFile = new File(DataFolder + "AnnotatedDocuments/" + controller.getCorpus().get(i).getName() + ".xml");
			output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(outputTestFile),"UTF-8"));
			// In the method toXML use "false" to use simple XML format (not GATE's XML).
			output.write("<?xml version='1.0' encoding='UTF-8'?>\r\n" + "<Document>" + controller.getCorpus().get(i).toXml(annotationsRequired, false) + "</Document>");
			output.close();

		}
		System.out.println("Proceso concluido");
	}
}
