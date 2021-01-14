import matplotlib.pyplot as plt
import os
import numpy as np
from tensorflow.keras.preprocessing import image
from model_trainer import model, cat1, cat0
dir_path = "dataset/test"
for i in os.listdir(dir_path):
    img = image.load_img(dir_path+"/"+i, target_size=(200, 200))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    val = model.predict(images)
    if val == 0:
        os.rename(dir_path+ "/"+ i, f"{dir_path}/{cat0}.{i}".replace(" ", "_"))
    else:
        os.rename(dir_path+"/" + i, f"{dir_path}/{cat1}.{i}".replace(" ", "_"))
