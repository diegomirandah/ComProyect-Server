print("training")
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt 
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Activation
from sklearn.metrics import confusion_matrix, classification_report 
import seaborn as sn
lr = 0.01

# crossing_arms_left
df_crossing_arms_left = pd.read_csv('dataset/Crossing_arms/left.csv',delimiter=";")
crossing_arms_left = df_crossing_arms_left.copy()
train_set_crossing_arms_left = crossing_arms_left.sample(frac=0.75, random_state=0)
test_set_crossing_arms_left = crossing_arms_left.drop(train_set_crossing_arms_left.index)

# crossing_arms_right
df_crossing_arms_right = pd.read_csv('dataset/Crossing_arms/right.csv',delimiter=";")
crossing_arms_right = df_crossing_arms_right.copy()
train_set_crossing_arms_right = crossing_arms_right.sample(frac=0.75, random_state=0)
test_set_crossing_arms_right = crossing_arms_right.drop(train_set_crossing_arms_right.index)

# hands_hip
df_hands_hip = pd.read_csv('dataset/hands_hip/hands_hip.csv',delimiter=";")
hands_hip = df_hands_hip.copy()
train_set_hands_hip = hands_hip.sample(frac=0.75, random_state=0)
test_set_hands_hip = hands_hip.drop(train_set_hands_hip.index)

# hands_to_head
df_hands_to_head = pd.read_csv('dataset/hands_to_head/hands_to_head.csv',delimiter=";")
hands_to_head = df_hands_to_head.copy()
train_set_hands_to_head = hands_to_head.sample(frac=0.75, random_state=0)
test_set_hands_to_head = hands_to_head.drop(train_set_hands_to_head.index)

# hug_opposite_arm_left
df_hug_opposite_arm_left = pd.read_csv('dataset/hug_opposite_arm/hug_opposite_arm_left.csv',delimiter=";")
hug_opposite_arm_left = df_hug_opposite_arm_left.copy()
train_set_hug_opposite_arm_left = hug_opposite_arm_left.sample(frac=0.75, random_state=0)
test_set_hug_opposite_arm_left = hug_opposite_arm_left.drop(train_set_hug_opposite_arm_left.index)

# hug_opposite_arm_right
df_hug_opposite_arm_right = pd.read_csv('dataset/hug_opposite_arm/hug_opposite_arm_right.csv',delimiter=";")
hug_opposite_arm_right = df_hug_opposite_arm_right.copy()
train_set_hug_opposite_arm_right = hug_opposite_arm_right.sample(frac=0.75, random_state=0)
test_set_hug_opposite_arm_right = hug_opposite_arm_right.drop(train_set_hug_opposite_arm_right.index)

# # Scratching_your_neck_left
# df_Scratching_your_neck_left = pd.read_csv('dataset/Scratching_your_neck/Scratching_your_neck_left.csv',delimiter=";")
# Scratching_your_neck_left = df_Scratching_your_neck_left.copy()
# train_set_Scratching_your_neck_left = Scratching_your_neck_left.sample(frac=0.75, random_state=0)
# test_set_Scratching_your_neck_left = Scratching_your_neck_left.drop(train_set_Scratching_your_neck_left.index)

# # Scratching_your_neck_right
# df_Scratching_your_neck_right = pd.read_csv('dataset/Scratching_your_neck/Scratching_your_neck_right.csv',delimiter=";")
# Scratching_your_neck_right = df_Scratching_your_neck_right.copy()
# train_set_Scratching_your_neck_right = Scratching_your_neck_right.sample(frac=0.75, random_state=0)
# test_set_Scratching_your_neck_right = Scratching_your_neck_right.drop(train_set_Scratching_your_neck_right.index)

# normal_posture
df_normal_posture = pd.read_csv('dataset/normal_posture/normal_posture.csv',delimiter=";")
normal_posture = df_normal_posture.copy()
train_set_normal_posture = normal_posture.sample(frac=0.75, random_state=0)
test_set_normal_posture = normal_posture.drop(train_set_normal_posture.index)

# hands_together
df_hands_together = pd.read_csv('dataset/hands_together/hands_together.csv',delimiter=";")
hands_together = df_hands_together.copy()
train_set_hands_together = hands_together.sample(frac=0.75, random_state=0)
test_set_hands_together = hands_together.drop(train_set_hands_together.index)

# Join data
train_set = pd.concat([
    train_set_crossing_arms_left, 
    train_set_crossing_arms_right, 
    train_set_hands_hip,
    train_set_hands_to_head,
    train_set_hug_opposite_arm_left,
    train_set_hug_opposite_arm_right,
    train_set_normal_posture,
    train_set_hands_together
    #train_set_Scratching_your_neck_left,
    #train_set_Scratching_your_neck_right
])
test_set = pd.concat([
    test_set_crossing_arms_left,
    test_set_crossing_arms_right,
    test_set_hands_hip, 
    test_set_hands_to_head,
    test_set_hug_opposite_arm_left,
    test_set_hug_opposite_arm_right,
    test_set_normal_posture,
    test_set_hands_together
    #test_set_Scratching_your_neck_left,
    #test_set_Scratching_your_neck_right
])


# print ('Training set')
print (train_set)
# print ('\nTest set')
print (test_set)

train_set_features = train_set.copy()
train_set_labels = train_set_features.pop('posture')

test_set_features = test_set.copy()
test_set_labels = test_set_features.pop('posture')

train_set_features = pd.DataFrame(train_set_features)
train_set_labels = pd.DataFrame(train_set_labels)

test_set_features = pd.DataFrame(test_set_features)
test_set_labels = pd.DataFrame(test_set_labels)

#creación

model = Sequential()
model.add(Dense(100, input_dim = 30))
model.add(Activation("relu"))
model.add(Dense(21))
model.add(Activation("relu"))
model.add(Dense(18))
model.add(Activation("relu"))
model.add(Dense(10))
model.add(Activation("softmax"))

# compilanción
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
#model.compile(loss='binary_crossentropy', optimizer= tf.optimizers.SGD(lr=lr), metrics=['acc'])

#entrenamiento
history = model.fit(train_set_features, train_set_labels, epochs=100, validation_data=[test_set_features,test_set_labels] )
model.save("softmax_Matrix3.h5")


# model = load_model("softmax_14282-4762_100.h5", compile = True)
# prediction = model.predict(tf.constant([[35.999107, 65.313774, 42.57383, 32.669384, 38.71361, 58.473003, 110.35055, 78.76348, 101.94205, 35.999107, 71.771935, 43.598892, 38.71361, 32.669384, 96.54847, 50.75069, 67.43754, 53.312298, 58.872543, 41.56628, 38.942097, 69.735115, 41.545063, 83.72377, 73.56506, 68.79059, 46.813343, 45.549088, 82.253944, 88.96795]]))
# print(prediction)
# clase = np.argmax(prediction, axis = 1)
# print(clase)

#evaluación
scores = model.evaluate(test_set_features, test_set_labels)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
print("%s: %.2f%%" % (model.metrics_names[0], scores[0]))
print("end")

# summarize history for accuracy
plt.plot(history.history['accuracy'], color='blue', label='train')
plt.plot(history.history['val_accuracy'], color='orange', label='test')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epochs')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('accuracy_matirx3.png')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'], color='blue', label='train')
plt.plot(history.history['val_loss'], color='orange', label='test')
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epochs')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('loss_matrix3.png')
plt.show()

print("matriz")
predictions = model.predict(test_set_features)  
print(len(np.argmax(predictions, axis = 1)))
print(len(test_set))
snn_cm = confusion_matrix(test_set_labels, np.argmax(predictions, axis = 1))
print(snn_cm)
snn_cm = snn_cm / snn_cm.astype(np.float).sum(axis=1)
print(snn_cm)
sn.heatmap(snn_cm, annot=True, fmt='.1%', cmap='Blues') # font size
plt.title('Confusion Matrix')
plt.ylabel('Observation')
plt.xlabel('Prediction')
plt.savefig('cf_matrix_matrix3.png')
plt.show()
