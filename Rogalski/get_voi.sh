#!/bin/bash

LOGFILE="logs.csv"
DOC_ID=1ierEhD6gcq51HAm433knjnVwey4ZE5DCnu1bW7PRG3E
SHEET_ID=1841152698
URL="https://docs.google.com/spreadsheets/d/$DOC_ID/export?format=csv&gid=$SHEET_ID"
DATAFILE="wojewodztwa.csv"
DATADIR=./Rogalski_data

cd $DATADIR
wget --output-file=$LOGFILE $URL -O $DATAFILE
cd ..

