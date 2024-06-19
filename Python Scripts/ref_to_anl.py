#import regular expression package
import re

#open input file
fin = open("data.txt", "rt")
#output file to write the result to
fout = open("out.txt", "wt")


##define a function which turns roman numerals into the corresponding digits.
def deromanize(number):
    number = number.upper().replace(" ", "")
    numerals = { 1000: "M", 900: "CM", 500: "D", 400: "CD", 100: "C", 90: "XC", 50: "L", 40: "XL", 10: "X", 9: "IX", 5: "V", 4: "IV", 1: "I" }
    result = 0
    for value in sorted(numerals, reverse=True):
        key = numerals[value]
        while (number.find(key) == 0):
            result += value
            number = number[len(key):]
    if result == 0:
    	return ""
    else:
    	return str(result)


#for each line in the input file
for line in fin:
#replace abbreviations for 'number' (N°, n°, #, no, No, with or without fullstops and spaces)
##when there is #/N°/n°/No/no at the beginning of the line (string) or after a space
##and followed by a full stop (optional), a space (optional) and one or several digits, then the abbreviation, the optional fullstop and space are replaced 
##by 'number'.
#	line=re.sub('no\.*\s*(\d+)|#\.*\s*(\d+)|N°\.*\s*(\d+)|n°\.*\s*(\d+)|No\.*\s*(\d+)', 'number \\1\\2\\3\\4\\5', line)
	line=re.sub('(\s+|^)(no|No|#|N°|n°)\.*\s*(\d+)', '\\1number \\3', line)

#if a line is not empty
	if len(line)>1:
#make roman numerals uppercase (even if they finish by 'j')
##if a series of letter which could potentially be a roman numeral appear after a space or in a new line and before a non-word character, they are capitalised.
		line=re.sub('((\s+|^)m{0,4}(cm|ccd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})j*\W)', lambda m: m.expand('\\1').upper(), line)
#delete '.' after roman numeral if it's NOT the end of the sentence.
##if a series of letter which could potentially be a roman numeral appear after a space or in a new line and NOT before a new line or a full stop followed by a 
##space and an uppercase letter, the full stop is deleted.
		line=re.sub('(((\s+|^)M{0,4}(CM|CCD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})J*)\.)(?!(\s[A-Z]|\n))', '\\2', line)
#replace j by i at the end of roman numeral.
##if a series of letter which could potentially be a roman numeral finishes by J and appears after a space or in a new line and before a non-word character, the
##J is turned into an I.
		line=re.sub('((\s+|^)M{0,4}(CM|CCD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))J(\W)', '\\1I\\6', line)


#delete the "." in cases such as 'St. Helen', 'Mr. Smith', 'Mrs. Smith', 'Ms. Smith'
##if Mrs, Mr, St, Ms are followed by a full stop, a space a capital letter (or 'and'), the full stop is deleted.
	line=re.sub('(Mrs|Mr|St|Ms)\.\s([A-Z]|and)', '\\1 \\2', line) 
#Write military titles in full.
##if a space or the beginning of the line is followed by the following abbreviations followed by a fullstop (optional), a space and a capital letter, the
##abbreviation is replaced by the full word and the fullstop is deleted.
	line=re.sub('(\s+|^)(Gov|GOV|gov)\.*\s([A-Z])', '\\1Governor \\3', line)
	line=re.sub('(\s+|^)(Sgt|SGT|sgt)\.*\s([A-Z])', '\\1Sergeant \\3', line)
	line=re.sub('(\s+|^)(Cpt|CPT|cpt)\.*\s([A-Z])', '\\1Captain \\3', line)
	line=re.sub('(\s+|^)(Capt|CAPT|capt)\.*\s([A-Z])', '\\1Captain \\3', line)
	line=re.sub('(\s+|^)(Maj|MAJ|maj)\.*\s([A-Z])', '\\1Major \\3', line)
	line=re.sub('(\s+|^)(Ltc|LTC|ltc)\.*\s([A-Z])', '\\1Lieutenant Colonel \\3', line)
	line=re.sub('(\s+|^)(Lt|LT|lt)\.*\s(Col|COL|col)\.*\s([A-Z])', '\\1Lieutenant Colonel \\4', line)
	line=re.sub('(\s+|^)(Col|COL|col)\.*\s([A-Z])', '\\1Colonel \\3', line)
	line=re.sub('(\s+|^)(Lt|LT|lt)\.*\s([A-Z])', '\\1Lieutenant \\3', line)
	line=re.sub('(\s+|^)(Lt|LT|lt)\.*\s(Gen|GEN|ge),\.*\s([A-Z])', '\\1Lieutenant Colonel \\4', line)
	line=re.sub('(\s+|^)(Gen|GEN|gen)\.*\s([A-Z])', '\\1General \\3', line)
	line=re.sub('(\s+|^)(Cmd|CMD|cmd)\.*\s([A-Z])', '\\1Commander \\3', line)
	line=re.sub('(\s+|^)(Ltg|LTG|ltg)\.*\s([A-Z])', '\\1Lieutenant General \\3', line)
	line=re.sub('(\s+|^)(Mme|MME|mme)\.*\s([A-Z])', '\\1Madame \\3', line)
#deal with abbreviations of inches and feet when they are preceded by digits.
##at the beginning of a line or after a space, if one (or several) digits are directly followed by ', followed by a space (optional), followed by another digit,
##transform ' in ft and " in ins (unless the number is 1, then inch).
	line=re.sub('(\s+|^)(\d+)\'\s*(1)\"', '\\1\\2 ft \\3 inch', line) 
	line=re.sub('(\s+|^)(\d+)\'\s*(\d+)\"', '\\1\\2 ft \\3 ins', line)
##at the beginning of a line or after a space, if one (or several) digits are directly followed by " or ', followed by a non-word character, transform ' in ft
##and " in ins (unless the number is 1, then inch).
	line=re.sub('(\s+|^)(\d+)\'(\W)', '\\1\\2 ft\\3', line)
	line=re.sub('(\s+|^)(1)\"(\W)', '\\1\\2 inch\\3', line)
	line=re.sub('(\s+|^)(\d+)\"(\W)', '\\1\\2 ins\\3', line)
#transform fraction written in superscript/subscript or in full letters into regular digits.
	line=re.sub('¾|three quarters', '3/4', line)
	line=re.sub('¼|one quarter', '1/4', line)
	line=re.sub('¾|three quarters', '3/4', line)
	line=re.sub('½', '1/2', line)
	line=re.sub('one third', '1/3', line)
	line=re.sub('two third', '2/3', line)
#



	fout.write(line)



#close input and output files
fin.close()
fout.close()
