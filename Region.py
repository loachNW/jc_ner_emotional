import re
import jieba
import numpy as np
from keras.layers import Embedding, Dense, Bidirectional, Conv1D, GRU, BatchNormalization, Activation, Dropout
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from sklearn.externals import joblib

from Attention import Attention
class Region(object):
    def __init__(self):
        self.tokenizer = joblib.load('tokenizer_final.model')
        self.model = self.cnn_rnn_attention()
        self.restr = r'[0-9\s+\.\!\/_,$%^*();?:\-<>《》【】+\"\']+|[+——！，；。？：、~@#￥%……&*（）]+'

    def cnn_rnn_attention(self):
        model = Sequential([
            Embedding(20000 + 1, 64, input_shape=(80,)),
            Conv1D(64, 3, padding='same'),
            BatchNormalization(),
            Activation('relu'),
            Bidirectional(GRU(128, return_sequences=True, reset_after=True), merge_mode='sum'),
            Attention(64),
            Dropout(0.5),
            Dense(2, activation='softmax')
        ])
        model.load_weights('model.h5')
        return model

    def prdected(self, text):
        resu = text.replace('|', '').replace('&nbsp;', '').replace('ldquo', '').replace('rdquo',
                                                                                        '').replace(
            'lsquo', '').replace('rsquo', '').replace('“', '').replace('”', '').replace('〔', '').replace('〕', '')
        resu = re.split(r'\s+', resu)
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', ''.join(resu))
        line = re.sub(self.restr, '', dd)
        seg_list = jieba.lcut(line)
        sequences = self.tokenizer.texts_to_sequences([seg_list])
        start = 0
        pred = []
        for i in range(int(len(sequences[0]) / 80) + 1):
            data = [sequences[0][start:start + 80]]
            data = pad_sequences(data, maxlen=80)
            pred.append(self.model.predict(data).tolist()[0][1])
            start += 80
        return 1 - np.mean(pred)