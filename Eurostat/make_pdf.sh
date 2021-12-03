cd $1
cd images
for filename in `(cat ../../file_list.txt)`
do
    rsvg-convert -f pdf -o $filename.pdf $filename.svg
done

pdfunite $(cat ../../file_list.txt | awk '{print $0".pdf"}') out.pdf

pdfjam --outfile out_a4.pdf --paper a4paper,landscape out.pdf 
pdfjam --outfile plots_a4_2x4.pdf --nup 2x4 out_a4.pdf
mv plots_a4_2x4.pdf ..
#rm *.pdf
cd ../..

