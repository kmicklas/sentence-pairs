import csv
import html
import sys
import wordfreq

if len(sys.argv) != 3:
    print('Usage: python3 sort.py target-lang pairs.csv')

targetLang = sys.argv[1]
pairsPath = sys.argv[2]

pairs = {}

with open(pairsPath, 'r', encoding='utf-8') as pairsFile:
    reader = csv.reader(pairsFile, delimiter='\t')
    for row in reader:
        words = wordfreq.tokenize(html.unescape(row[0]), targetLang)

        freqs = [wordfreq.zipf_frequency(word, targetLang, wordlist='combined')
                     for word in words]

        minfreq = min(freqs)
        avgfreq = sum(freqs) / float(len(freqs))
        pairs[row[0]] = (minfreq, avgfreq, row[1])

pairList = list(pairs.items())
pairList.sort(reverse = True, key=lambda i: i[1])

for pair in pairList:
    sys.stdout.buffer.write((pair[0] + '\t' + pair[1][2] + '\n').encode('utf-8'))
