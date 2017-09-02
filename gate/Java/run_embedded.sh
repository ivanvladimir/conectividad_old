#! /bin/bash
# autor: @Penserbjorne - Sebastian Aguilar
# FI-IIMAS-IIJ-UNAM

echo "Executing..."

DFLAGS1=-Dgate.home=$GATE_HOME
DFLAGS2=-Dgate.plugins.home=$GATE_HOME/plugins
DFLAGS3=-Dgate.site.config=$GATE_HOME/gate.xml

echo "GateEmbedded flags: " $DFLAGS1 $DFLAGS2 $DFLAGS3

java $DFLAGS1 $DFLAGS2 $DFLAGS3 -cp $CP GateEmbedded

echo ""
