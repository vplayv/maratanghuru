from tensorflow import models
from tensorflow import layers
from tensorflow import optimizers
from tensorflow import losses
from tensorflow import metrics
import nltk

def my_modeling(train_docs, test_docs):
    '''
    train_docs : my_train 첫번쨰 결과값
    test_docs : my_train 두번쨰 결과값
    '''
    
    '''전처리기 설정'''
    text = nltk.Text(tokens, name='NMSC')
    
    '''데이터 모델링 상수'''
    WORD_COUNT = 100
    
    # 시간이 꽤 걸립니다! 시간을 절약하고 싶으면 most_common의 매개변수를 줄여보세요.
    selected_words = [f[0] for f in text.vocab().most_common(WORD_COUNT)]
    
    def term_frequency(doc):
        return [doc.count(word) for word in selected_words]
    
    train_x = [term_frequency(d) for d, _ in train_docs]
    test_x  = [term_frequency(d) for d, _ in test_docs]
    
    train_y = [c for _, c in train_docs]
    test_y  = [c for _, c in test_docs]
    
    x_train = np.asarray(train_x).astype('float32')
    x_test = np.asarray(test_x).astype('float32')

    y_train = np.asarray(train_y).astype('float32')
    y_test = np.asarray(test_y).astype('float32')
    
    '''리턴 값 훈련모델 x, y축'''
    
    '''데이터 모델링 상수'''
    WORD_COUNT = 100
    
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu', input_shape=(WORD_COUNT,)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))

    model.compile(optimizer=optimizers.RMSprop(lr=0.001),
                loss=losses.binary_crossentropy,
                metrics=[metrics.binary_accuracy])

    model.fit(x_train, y_train, epochs=10, batch_size=512)

    results = model.evaluate(x_test, y_test)