from keras.models import Sequential


# Keras의 레이어들을 구성하는 방법으로 사용되는 핵심적인 자료구조형은 model임.
# 그 중 가장 간단한 형태의 모델은 레이어를 선형으로 쌓는 Sequential model.
# 더 복잡한 구조를 원한다면 Keras의 레이어의 임의의 그래프를 작성할 수 있는 functional API를 사용할 수 있음.
model = Sequential()

from keras.layers import Dense

# 레이어는 다음과 같이 .add()를 통해 추가할 수 있음
# units? activation? input_dim?
model.add(Dense(units=64, activation='relu', input_dim=100))
model.add(Dense(units=10, activation='softmax'))

# 모델이 어느 정도 모양을 갖추면, .compile()을 통해 학습 방법을 설정할 수 있음.
model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])

# 프로그래머가 원한다면 더 복잡하게 최적화(optimizer parameter) 설정 등을 할 수 있음
# Keras의 궁극적인 원칙 상황을 간편하게 하고 사용자에게 필요한 모든 제어권을 주는 것임
# 사용자가 필요한 상황에서 모든 제어권을 가지고 있다는 말은 코드의 확장성이 좋다는 말과 같음
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True))

# 모델 컴파일까지 완료되면 이제 학습시킬 수 있음
model.fit(x_train, y_train, epochs=5, batch_size=32)

# 또는 배치에 수동으로 모델에 피드를 줄 수 있음
model.train_on_batch(x_batch, y_batch)

# 한 줄로 모델 평가 가
loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)

# 예측도 가능
classes = model.predict(x_test, batch_size=128)
