import csv
import html
import sys

if len(sys.argv) < 4:
    print('Usage: python3 find-pairs.py [--allow-empty-translations] ' +
          'sentences.csv links.csv target-language translation-languages...')
    sys.exit(1)

args = sys.argv[1:]

allowEmptyTranslations = False
if args[0] == '--allow-empty-translations':
    allowEmptyTranslations = True
    args = args[1:]

sentencesPath = args[0]
linksPath = args[1]
targetLang = args[2]
transLangs = args[3:]

targetSents = {}
transSents = {}

# Find all target language sentences and allowed direct translations
with open(sentencesPath, 'r', encoding='utf-8') as sentenceFile:
    reader = csv.reader(sentenceFile, delimiter='\t')
    for row in reader:
        if row[1] == targetLang:
            targetSents[row[0]] = (row[2], [])
        elif row[1] in transLangs:
            transSents[row[0]] = row[2]

# Find translations of target sentences
with open(linksPath, 'r', encoding='utf-8') as linksFile:
    reader = csv.reader(linksFile, delimiter='\t')
    for row in reader:
        if row[0] in targetSents and row[1] in transSents:
            targetSents[row[0]][1].append(transSents[row[1]])

# Print out all target sentences and their translations
for (ident, (target, trans)) in targetSents.items():
    if allowEmptyTranslations or len(trans) > 0:
        sys.stdout.buffer.write(
            (html.escape(target) + '\t' +
            '<br>'.join([html.escape(s) for s in trans]) + '\n').encode('utf-8'))
