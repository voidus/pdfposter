#!/bin/bash
#
# Usage:
#  make-thumbs.sh [options] COLUMNS PDFFILENAME
#
# Options:
#   -p... will be passed to pdfposter
#   -m... will be passed to pdfposter
#   -A    will be passed to pdfposter (--art-box)
#   -R    rotate page-thumbs prior to montaging the image
#
# Example:
#    make-thumbs.sh -p2x2A4    2 test/allboxes.pdf
#    make-thumbs.sh -p3x2A4 -R 2 test/allboxes.pdf
#
# This uses pdftoppm, which uses poppler instead of ImageMagick's
# convert, which uses ghostscript, since poppler is much more
# tolerant.
#

SCALE=200
BGCOLOR=bisque2
BORDER=3

posterargs=
while getopts "Ap:m:R" opt; do
    case $opt in
	p|m)
	    posterargs="$posterargs -$opt$OPTARG"
	    ;;
	A)
	    posterargs="$posterargs -$opt"
	    ;;
	R)
	    rotate="-rotate -90"
	    ;;
	\?)
	    echo "Invalid option: -$OPTARG" >&2
	    ;;
    esac
done

shift $((OPTIND-1))
cols="${1:?Required argument COLUMNS missing}" ; shift
pdfname="${1:?Required argument PDFFILENAME missing}"

declare -a inpngs outpngs

bname=$TMP/$(basename "$pdfname" .pdf)

./pdfposter $posterargs $pdfname $bname-1.pdf

pdftoppm -png -scale-to $SCALE $bname-1.pdf $bname-1
inpngs=( $bname-1*.png )

rows=$(( ${#inpngs[@]} / cols ))
outname="$bname-${rows}x${cols}.png"

if [ "$rows" -eq 1 -a "$cols" -eq 1 ] ; then
    BORDER=$((BORDER*2))
fi

montage "${inpngs[@]}" $rotate -geometry +$BORDER+$BORDER \
    -background $BGCOLOR -tile 1x${rows} miff:- \
    | convert - +append miff:- \
    | montage - -geometry +$BORDER+$BORDER -background $BGCOLOR "$outname"

rm $bname-1*.png
echo created $outname
