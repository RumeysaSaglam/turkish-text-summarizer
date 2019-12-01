"""
Zemberek: Python Interface for Zemberek Jar
Inspired by: https://bit.ly/2JopMvt

Authors: Medine Aktaş, Rümeysa Sağlam
Email: medneaktas@gmail.com, rumeysasaglam98@gmail.com
"""

from os.path import join
from jpype import JClass, getDefaultJVMPath, shutdownJVM, startJVM, JString, java


class zemberek(object):
    def __init__(self):
        ZEMBEREK_PATH: str = join('..', '..', 'bin', 'zemberek-full.jar')

        startJVM(
            getDefaultJVMPath(),
            '-ea',
            f'-Djava.class.path={ZEMBEREK_PATH}',
            convertStrings=False
        )


    def sent_Tokenize(self, paragraph):
        TurkishSentenceExtractor: JClass = JClass(
            'zemberek.tokenization.TurkishSentenceExtractor'
        )

        extractor: TurkishSentenceExtractor = TurkishSentenceExtractor.DEFAULT

        sentences = extractor.fromParagraph((
            paragraph
        ))

        for i, word in enumerate(sentences):
            print(f'Sentence {i + 1}: {word}')


    def word_Tokenize(self, inp):
        Token: JClass = JClass('zemberek.tokenization.Token')
        TurkishTokenizer: JClass = JClass('zemberek.tokenization.TurkishTokenizer')

        tokenizer: TurkishTokenizer = TurkishTokenizer.DEFAULT
        tokenizer: TurkishTokenizer = TurkishTokenizer.builder().ignoreTypes(
            Token.Type.Punctuation,
            Token.Type.NewLine,
            Token.Type.SpaceTab

        ).build()

        print(f'Input = {inp} ')
        for i, token in enumerate(tokenizer.tokenize(JString(inp))):
            print(f' | Token {i} = {token.getText()}')

    def stem(self,word):
        TurkishMorphology: JClass = JClass('zemberek.morphology.TurkishMorphology')
        WordAnalysis: JClass = JClass('zemberek.morphology.analysis.WordAnalysis')

        morphology: TurkishMorphology = TurkishMorphology.createWithDefaults()

        print(f'\nWord: {word}\n\nResults:')

        results: WordAnalysis = morphology.analyze(JString(word))

        for result in results:
            print(
                f'{str(result.formatLong())}'
                f'\n\tStems ='
                f' {", ".join([str(result) for result in result.getStems()])}'
                f'\n\tLemmas ='
                f' {", ".join([str(result) for result in result.getLemmas()])}'
            )


    def stopWords(self):
        text_file = open("stop-words.tr.txt", "r")
        lines = text_file.readlines()

        text_file.close()
        return lines

    def __del__(self):
        shutdownJVM()


if __name__ == '__main__':
    paragraph = 'Prof. Dr. Veli Davul açıklama yaptı. Kimse %6.5 lik enflasyon oranını beğenmemiş!    Oysa maçta ikinci olmuştuk... Değil mi?'
    zmbrk = zemberek()
    zmbrk.sent_Tokenize(paragraph)

    str_ = 'Saat, 12:00'
    zmbrk.word_Tokenize(str_)
    word = 'kutucuğumuz'

    zmbrk.stem(word)
    lines = zmbrk.stopWords()
    print(lines)
    print(len(lines))