import joblib
from konlpy.tag import Okt
from .ordermenu import orderParsing

okt = Okt()
tokenizer = joblib.load("./token.pkl")
rnd_clf = joblib.load("./nlp_sample.pkl")
pad_sequences = joblib.load("./pad_sequences.pkl")


# 띄어쓰기 함수
def spacing_okt(wrongSentence):
    tagged = okt.pos(wrongSentence)
    corrected = ""
    for i in tagged:
        # print(i)
        if i[1] in ('Josa', 'PreEomi', 'Eomi', 'Suffix', 'Punctuation', 'Modifier'):
            corrected += i[0]
        else:
            corrected += " "+i[0]
    if corrected[0] == " ":
        corrected = corrected[1:]
    return corrected


# 처음 보는 문장 검사
def check_new_text(text):
    for x in text:
        if int(x) > 1:
            return True
    return False


def rndModel(new_sentence):
    stopwords = ['메뉴', '보이다', '줄다', '이요', '요', '의', '로', '가', '이', '은', '들', '는', '좀',
                 '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다', '저기요', '주세요', '할게요', '하세요', '주다']
    # global order_data
    text = new_sentence
    new_sentence = spacing_okt(new_sentence)
    print(new_sentence)
    new_sentence = new_sentence.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
    # 토큰화
    new_sentence = okt.morphs(new_sentence, stem=True)

    # 불용어 제거
    new_sentence = [word for word in new_sentence if not word in stopwords]

    # 정수 인코딩
    encoded = tokenizer.texts_to_sequences([new_sentence])
    print(new_sentence)
    # print(encoded)

    if check_new_text(encoded[0]) == False:
        print("이해할수 없는 단어")

    else:
        deleteList = []
        for x in range(len(encoded[0])):
            if encoded[0][x] == 1:
                deleteList.append(x)
        deleteList.sort(reverse=True)

        if len(deleteList):
            for x in deleteList:
                encoded[0].pop(x)
        # 패딩
        pad_new = pad_sequences(encoded, maxlen=4)
        # print(pad_new)

        # 예측
        # score = float(rnd_clf.predict(pad_new))
        # print(score)
        result = rnd_clf.predict(pad_new)
        print(result[0])
        result_set = {'result': int(result[0])}
        name = ""
        if result[0] == 9:
            result_set = orderParsing(text)
        elif result[0] == 3:
            if text.find("매장") != -1:
                name = "매장"
            if text.find("포장") != -1:
                name = "포장"
            result_set = {'result': int(result[0]), '0': {'name': name}}
        print(result_set)
        return result_set


if __name__ == "__main__":
    while(1):
        temp = input()
        if(temp == 'stopModel'):
            joblib.dump(tokenizer, 'token.pkl')
            joblib.dump(rnd_clf, 'nlp_sample.pkl')
            joblib.dump(rndModel, 'rndModel')
            break
        else:
            rndModel(temp)
