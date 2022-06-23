import numpy as np
from keras.models import load_model
from PIL import Image
from PIL import ImageOps


def recognition_sign(path_to_img):
    name_sing = [
        'Скользкая дорога',
        'Дикие животные',
        'Главная дорога',
        'Въезд запрещен',
        'Пешеходное движение запрещено',
        'Обгон запрещен',
        'Одностороннее движение',
        'Пешеходный переход',
        'Парковочное место',
        'Тупик',
    ]

    model = load_model('./app/recognition/keras_model.h5')

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open(path_to_img)

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)

    for index in prediction:
        i = np.argmax(index)
        for j in name_sing:
            if i == name_sing.index(j):
                return name_sing[i]
