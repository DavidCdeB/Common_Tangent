#!/bin/bash
\rm *.blg *.bbl *.dvi *.aux *.log #lab_report_1.pdf
pdflatex -shell-escape lab_report_1
bibtex lab_report_1 
pdflatex -shell-escape lab_report_1
pdflatex -shell-escape lab_report_1
bibtex lab_report_1 
pdflatex -shell-escape lab_report_1
#dvips lab_report_1.dvi 
#ps2pdf lab_report_1.ps
#okular lab_report_1.pdf
