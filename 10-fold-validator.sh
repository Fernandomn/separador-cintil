#!/bin/bash

getTrainingBlock(){
  case $1 in 
    0) echo "$(($blockSize+1))-$qntFiles";;
    9) echo "1-$(($1*$blockSize))";;
    *) echo "1-$(($count*$blockSize)),$(((($count+1)*$blockSize)+1))-$qntFiles";;
  esac
}

cd "~/projeto-final-parsers/stanford-parser-full-2017-06-09/"
qntFolds=10
dir='/home/fernando/projeto-final-parsers/cintil/separador-cintil/tree-trad'
qntFiles=`ls -1 $dir | wc -l`
count=0
blockSize=$((qntFiles/qntFolds))
jarFile="~/projeto-final-parsers/stanford-parser-full-2017-06-09/stanford-parser.jar"
memAmmout="-mx4g"
nameParser="edu.stanford.nlp.parser.lexparser.LexicalizedParser"
serializedGrammarFilename="~/projeto-final-parsers/serialized-files/serialCINTIL"
outputFormat='"wordsAndTags,penn,typedDependencies"'
# outputFormatOptions=
# outputFilesExtension=
outputFilesDirectory="~/projeto-final-parsers/stanford-parser-full-2017-06-09/outputs/treinoCINTIL/treino"

while (("$count" < "$qntFolds")); do
  testBlock="$((($count*$blockSize)+1))-$(($(($count+1))*$blockSize))"
  trainingBlock=$(getTrainingBlock $count )

  trainFilesPath="~/projeto-final-parsers/cintil/separador-cintil/tree-trad $trainingBlock"
  testFilePath="~/projeto-final-parsers/cintil/separador-cintil/tree-trad $testBlock"
  resultFile="~/projeto-final-parsers/outputs/treinoCINTIL/treino$(($count+1)).txt"

  trainingCmd="java -cp $jarFile $memAmmout $nameParser 
  -train $trainFilesPath
  -test  $testFilePath
  -saveToSerializedFile $serializedGrammarFilename
  -writeOutputFiles
  -outputFormat $outputFormat
  -outputFilesDirectory $outputFilesDirectory
  > $resultFile"

  echo $trainingCmd
  # $trainingCmd

  count=$(($count + 1))
done