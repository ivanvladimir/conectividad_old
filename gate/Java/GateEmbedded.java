/*
 *  BatchProcessApp.java
 *
 *
 * Copyright (c) 2006, The University of Sheffield.
 *
 * This file is part of GATE (see http://gate.ac.uk/), and is free
 * software, licenced under the GNU Library General Public License,
 * Version 2, June1991.
 *
 * A copy of this licence is included in the distribution in the file
 * licence.html, and is also available at http://gate.ac.uk/gate/licence.html.
 *
 *  Ian Roberts, March 2006
 *
 *  $Id: BatchProcessApp.java,v 1.5 2006/06/11 19:17:57 ian Exp $

 *  modified: @Penserbjorne - Sebastian Aguilar
 *  FI-IIMAS-IIJ-UNAM
 */

import gate.Document;
import gate.Corpus;
import gate.CorpusController;
import gate.AnnotationSet;
import gate.Gate;
import gate.Factory;
import gate.util.*;
import gate.util.persistence.PersistenceManager;

import java.util.Set;
import java.util.HashSet;
import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;

import java.io.File;
import java.io.FileOutputStream;
import java.io.BufferedOutputStream;
import java.io.OutputStreamWriter;

/**
 * This class ilustrates how to do simple batch processing with GATE.  It loads
 * an application from a .gapp file (created using "Save application state" in
 * the GATE GUI), and runs the contained application over one or more files.
 * The results are written out to XML files, either in GateXML format (all
 * annotation sets preserved, as in "save as XML" in the GUI), or with inline
 * XML tags taken from the default annotation set (as in "save preserving
 * format").  In this example, the output file names are simply the input file
 * names with ".out.xml" appended.
 *
 * To keep the example simple, we do not do any exception handling - any error
 * will cause the process to abort.
 */
public class GateEmbedded {

  /**
   * The main entry point.  First we parse the command line options (see
   * usage() method for details), then we take all remaining command line
   * parameters to be file names to process.  Each file is loaded, processed
   * using the application and the results written to the output file
   * (inputFile.out.xml).
   */
  public static void main(String[] args) throws Exception {
    parseCommandLine(args);

    System.out.println("Getting all documents to process.");
    filesToUse = listf(DataFolder + "extract_text/");

    // initialise GATE - this must be done before calling any GATE APIs
    System.out.println("Prepare the library.");
    Gate.init();

		System.out.println("Get the root plugins dir.");
		File pluginsDir = Gate.getPluginsHome();

    // load the saved application
    System.out.println("Load saved GATE app.");
    CorpusController application = (CorpusController)PersistenceManager.loadObjectFromFile(gappFile);

    // Create a Corpus to use.  We recycle the same Corpus object for each
    // iteration.  The string parameter to newCorpus() is simply the
    // GATE-internal name to use for the corpus.  It has no particular
    // significance.
    System.out.println("Create a corpus.");
    Corpus corpus = Factory.newCorpus("BatchProcessApp Corpus");
    application.setCorpus(corpus);

		System.out.println("Adding AnnotTypesRequired.");
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

    System.out.println("Process the files one by one");
    // process the files one by one
    Iterator iterFiles = filesToUse.iterator();

    //for(int i = firstFile; i < args.length; i++) {
    while(iterFiles.hasNext()) {
      try{
        // load the document (using the specified encoding if one was given)
        //File docFile = new File(args[i]);
        File docFile = (File)iterFiles.next();
        System.out.println("Processing document " + (processedFiles+1) + " of " + filesToUse.size() + ": " + docFile + "...");
        Document doc = Factory.newDocument(docFile.toURL(), encoding);

        System.out.println("\tAdding to corpus and executing.");
        // put the document in the corpus
        corpus.add(doc);

        // run the application
        application.execute();

        // remove the document from the corpus again
        corpus.clear();

        String docXMLString = null;

        System.out.println("\tExtracting annotations.");

        // Create a temporary Set to hold the annotations we wish to write out
        Set annotationsToWrite = new HashSet();

        // we only extract annotations from the default (unnamed) AnnotationSet
        // in this example
        AnnotationSet defaultAnnots = doc.getAnnotations();
        Iterator annotTypesIt = annotTypesRequired.iterator();
        while(annotTypesIt.hasNext()) {
          // extract all the annotations of each requested type and add them to
          // the temporary set
          AnnotationSet annotsOfThisType = defaultAnnots.get((String)annotTypesIt.next());
          if(annotsOfThisType != null) {
            annotationsToWrite.addAll(annotsOfThisType);
          }
        }

        System.out.println("\tCreating XML file.");
        // create the XML string using these annotations
        docXMLString = doc.toXml(annotationsToWrite, false);

        // Release the document, as it is no longer needed
        Factory.deleteResource(doc);

        // output the XML to <inputFile>.out.xml
        String outputFileName = "/../annotatedDocuments/" + docFile.getName() + ".xml";
        File outputFile = new File(docFile.getParentFile(), outputFileName);

        System.out.println("\tWriting XML file on " + outputFile);
        // Write output files using the same encoding as the original
        FileOutputStream fos = new FileOutputStream(outputFile);
        BufferedOutputStream bos = new BufferedOutputStream(fos);
        OutputStreamWriter out;
        if(encoding == null) {
          out = new OutputStreamWriter(bos);
        }
        else {
          out = new OutputStreamWriter(bos, encoding);
        }

        //out.write("<?xml version='1.0' encoding='UTF-8'?>\r\n" + "<Document>" + docXMLString + "</Document>");
        out.write(docXMLString);

        out.close();
        System.out.println("\tDone current document.");
        processedFiles++;

        docFile = null;
        doc = null;
        docXMLString = null;
        annotationsToWrite = null;
        defaultAnnots = null;
        annotTypesIt = null;
        outputFileName = null;
        outputFile = null;
        fos = null;
        bos = null;
        out = null;
        System.gc();
      }catch(OutOfMemoryError e){
        System.out.println("Error of memory!");
        System.gc();
      }
    } // for each file

    System.out.println("All done!!!");
    System.out.println(processedFiles + " files processed.");
  } // void main(String[] args)


  /**
   * Get all files from a Directory.
   */
   private static List<File> listf(String directoryName) {
       File directory = new File(directoryName);
       List<File> resultList = new ArrayList<File>();
       // get all the files from a directory
       File[] fList = directory.listFiles();
       //resultList.addAll(Arrays.asList(fList));
       for (File file : fList) {
         if(file.isFile()){
           resultList.add(file);
         }else if(file.isDirectory()) {
           resultList.addAll(listf(file.getAbsolutePath()));
         }
       }
       return resultList;
   }

  /**
   * Parse command line options.
   */
  private static void parseCommandLine(String[] args) throws Exception {
    int i;
    // iterate over all options (arguments starting with '-')
    for(i = 0; i < args.length && args[i].charAt(0) == '-'; i++) {
      switch(args[i].charAt(1)) {
        // -g gappFile = path to the saved application
        case 'g':
          gappFile = new File(args[++i]);
          break;

        // -e encoding = character encoding for documents
        case 'e':
          encoding = args[++i];
          break;

        default:
          System.err.println("Unrecognised option " + args[i]);
          usage();
      }
    }

    // set index of the first non-option argument, which we take as the first
    // file to process
    //firstFile = i;

    // sanity check other arguments
    if(gappFile == null) {
      System.err.println("No .gapp file specified");
      usage();
    }
  }

  /**
   * Print a usage message and exit.
   */
  private static final void usage() {
    System.err.println(
   "Usage:\n" +
   "   BatchProcessApp -g <gappFile> [-e encoding] [-a annotType]\n" +
   "             [-a annotType] file1 file2 ... fileN\n" +
   "\n" +
   "-g gappFile : (required) the path to the saved application state we are\n" +
   "              to run over the given documents.  This application must be\n" +
   "              a \"corpus pipeline\" or a \"conditional corpus pipeline\".\n" +
   "\n" +
   "-e encoding : (optional) the character encoding of the source documents.\n" +
   "              If not specified, the platform default encoding (currently\n" +
   "              \"" + System.getProperty("file.encoding") + "\") is assumed.\n"
   );

    System.exit(1);
  }

  /** Index of the first non-option argument on the command line. */
  //private static int firstFile = 0;
  private static int processedFiles = 0;

  /** Path to the saved application file. */
  private static File gappFile = null;

  /**
   * List of annotation types to write out.  If null, write everything as
   * GateXML.
   */
  private static Set<String> annotTypesRequired = new HashSet<String>();

  /** Folder where is the data to process*/
  private static String DataFolder = "./../../src/python/data/";

  /** To get Files from directory*/
  private static List<File> filesToUse = null;

  /**
   * The character encoding to use when loading the docments.  If null, the
   * platform default encoding is used.
   */
  private static String encoding = null;
}
