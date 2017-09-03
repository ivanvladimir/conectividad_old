#! /bin/bash
# autor: @Penserbjorne - Sebastian Aguilar
# FI-IIMAS-IIJ-UNAM

# Define a timestamp function
timestamp() {
  date +"%T"
}

echo $(timestamp) " > Executing"

CP=.:$GATE_HOME/bin:$GATE_HOME/bin/gate.jar:$GATE_HOME/lib/ant-1.9.3.jar:$GATE_HOME/lib/ant-launcher-1.9.3.jar:$GATE_HOME/lib/aopalliance-1.0.jar:$GATE_HOME/lib/apache-mime4j-core-0.7.2.jar:$GATE_HOME/lib/apache-mime4j-dom-0.7.2.jar:$GATE_HOME/lib/bcmail-jdk15-1.45.jar:$GATE_HOME/lib/bcprov-jdk15-1.45.jar:$GATE_HOME/lib/commons-codec-1.9.jar:$GATE_HOME/lib/commons-compress-1.8.1.jar:$GATE_HOME/lib/commons-io-2.4.jar:$GATE_HOME/lib/commons-lang-2.6.jar:$GATE_HOME/lib/commons-logging-1.1.3.jar:$GATE_HOME/lib/flying-saucer-core-9.0.4.jar:$GATE_HOME/lib/fontbox-1.8.8.jar:$GATE_HOME/lib/gate-asm-5.0.3.jar:$GATE_HOME/lib/gate-compiler-jdt-4.3.2-P20140317-1600.jar:$GATE_HOME/lib/hamcrest-core-1.3.jar:$GATE_HOME/lib/ivy-2.3.0.jar:$GATE_HOME/lib/ivy-report.css:$GATE_HOME/lib/jackson-annotations-2.3.0.jar:$GATE_HOME/lib/jackson-core-2.3.2.jar:$GATE_HOME/lib/jackson-databind-2.3.2.jar:$GATE_HOME/lib/java-getopt-1.0.13.jar:$GATE_HOME/lib/jaxen-1.1.6.jar:$GATE_HOME/lib/jdom-1.1.3.jar:$GATE_HOME/lib/jempbox-1.8.8.jar:$GATE_HOME/lib/joda-time-2.9.2.jar:$GATE_HOME/lib/junit-4.11.jar:$GATE_HOME/lib/log4j-1.2.17.jar:$GATE_HOME/lib/nekohtml-1.9.14.jar:$GATE_HOME/lib/pdfbox-1.8.8.jar:$GATE_HOME/lib/poi-3.11.jar:$GATE_HOME/lib/poi-ooxml-3.11.jar:$GATE_HOME/lib/poi-ooxml-schemas-3.11.jar:$GATE_HOME/lib/poi-scratchpad-3.11.jar:$GATE_HOME/lib/spring-aop-2.5.6.SEC01.jar:$GATE_HOME/lib/spring-beans-2.5.6.SEC01.jar:$GATE_HOME/lib/spring-core-2.5.6.SEC01.jar:$GATE_HOME/lib/stax2-api-3.1.1.jar:$GATE_HOME/lib/tika-core-1.7.jar:$GATE_HOME/lib/tika-parsers-1.7.jar:$GATE_HOME/lib/woodstox-core-lgpl-4.2.0.jar:$GATE_HOME/lib/xercesImpl-2.9.1.jar:$GATE_HOME/lib/xmlbeans-2.6.0.jar:$GATE_HOME/lib/xmlunit-1.5.jar:$GATE_HOME/lib/xpp3-1.1.4c.jar:$GATE_HOME/lib/xstream-1.4.7.jar

DFLAGS1=-Dgate.home=$GATE_HOME
DFLAGS2=-Dgate.plugins.home=$GATE_HOME/plugins
DFLAGS3=-Dgate.site.config=$GATE_HOME/gate.xml

echo "GateEmbedded flags: " $DFLAGS1 $DFLAGS2 $DFLAGS3

java $DFLAGS1 $DFLAGS2 $DFLAGS3 -cp $CP GateEmbedded

echo $(timestamp) " > Execution terminated"

echo ""
