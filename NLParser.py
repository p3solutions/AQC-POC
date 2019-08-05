import os

from nltk.parse.stanford import StanfordDependencyParser
from nltk.tag.stanford import StanfordPOSTagger


class NLParser:
    java_path = "/Library/Java/JavaVirtualMachines/jdk1.8.0_152.jdk/Contents/Home"
    os.environ['JAVAHOME'] = java_path
    os.environ['STANFORD_MODELS'] = '../lib/stanford/stanfordstanford-postagger-full-2016-10-31/models/english-caseless-left3words-distsim.tagger:' \
                             '../lib/stanford/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar:' \
                             '../lib/stanford/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models/edu/stanford/nlp/models/parser/nndep/english_UD.gz'
    os.environ['CLASSPATH'] = '../lib/stanford/stanford-parser-full-2016-10-31/stanford-parser.jar:' \
                              '../lib/stanford/stanford-postagger-full-2016-10-31/stanford-postagger.jar:' \
                              '../lib/stanford/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar:' \
                              '../lib/stanford/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models/edu/stanford/nlp/models/parser/nndep/english_UD.gz'

    sentence = 'This is just for testing'

    tagger = None
    parser = None

    def __init__(self):
        path_to_model_tagger = "../lib/stanford/stanford-postagger-full-2016-10-31/models/english-caseless-left3words-distsim.tagger"
        path_to_jar_tagger = "../lib/stanford/stanford-postagger-full-2016-10-31/stanford-postagger.jar"
        NLParser.tagger = StanfordPOSTagger(path_to_model_tagger, path_to_jar_tagger)
        NLParser.tagger.java_options = '-mx4096m'  ### Setting higher memory limit for long sentences
        NLParser.parser = StanfordDependencyParser(
            path_to_jar='../lib/stanford/stanford-parser-full-2016-10-31/stanford-parser.jar')
        print ("Parser Initialized.........")
        NLParser.parser.raw_parse(self.sentence)

        # print [parse.tree() for parse in self.parser.raw_parse("The quick brown fox jumps over the lazy dog.")]
        # print self.tagger.tag(self.sentence.split())

# a = NLParser()
