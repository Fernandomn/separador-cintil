#!/bin/bash

getTrainingBlock() {
  case $1 in
  0) echo "$(($blockSize + 1))-$qntFiles" ;;
  9) echo "1-$(($1 * $blockSize))" ;;
  *) echo "1-$(($count * $blockSize)),$(((($count + 1) * $blockSize) + 1))-$qntFiles" ;;
  esac
}

cd $HOME/projeto-final-parsers/stanford-parser-full-2017-06-09
mkdir $HOME/projeto-final-parsers/stanford-parser-full-2017-06-09/output/treinoCINTIL/treino

qntFolds=10
dir="$HOME/projeto-final-parsers/cintil/separador-cintil/tree-trad"
qntFiles=$(ls -1 $dir | wc -l)
count=0
blockSize=$((qntFiles / qntFolds))
jarFile="stanford-parser.jar"
# jarFile="$HOME/projeto-final-parsers/stanford-parser-full-2017-06-09/stanford-parser.jar"
memAmmout="-mx4g"
nameParser="edu.stanford.nlp.parser.lexparser.LexicalizedParser"
serializedGrammarFilename="$HOME/projeto-final-parsers/serialized-files/serialCINTIL"
outputFormat='wordsAndTags,penn,typedDependencies'
mkdir -p $HOME/projeto-final-parsers/outputs/treinoCINTIL/treino
outputFilesDirectory="$HOME/projeto-final-parsers/outputs/treinoCINTIL/treino"
# outputFormatOptions=
# outputFilesExtension=

while (("$count" < "$qntFolds")); do
  testBlock="$((($count * $blockSize) + 1))-$(($(($count + 1)) * $blockSize))"
  trainingBlock=$(getTrainingBlock $count)

  trainFilesPath="$HOME/projeto-final-parsers/cintil/separador-cintil/tree-trad $trainingBlock"
  testFilePath="$HOME/projeto-final-parsers/cintil/separador-cintil/tree-trad $testBlock"
  mkdir -p $HOME/projeto-final-parsers/outputs/treinoCINTIL
  resultFile="$HOME/projeto-final-parsers/outputs/treinoCINTIL/treino$(($count + 1)).txt"
  outputFormatOptions='lexicalize'
  nthreads=-1

  trainingCmd="java -cp $jarFile $memAmmout $nameParser 
  -train $trainFilesPath
  -test  $testFilePath
  -saveToSerializedFile $serializedGrammarFilename
  -writeOutputFiles
  -outputFormat $outputFormat
  -outputFormatOptions $outputFormatOptions
  -nthreads $nthreads
  -outputFilesDirectory $outputFilesDirectory
  "
  # > $resultFile

  echo $trainingCmd
  $trainingCmd | tee $resultFile

  count=$(($count + 1))
done
