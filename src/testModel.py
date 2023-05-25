import time

import numpy as np
import scipy
from keras import optimizers

from models import SiameseModel
from utils import load_data, recall_at_k

# --- Set global variables --- #
BATCH_SIZE = 16
EPOCHS = 10
WEIGHTS_PATH = "/tf/notebooks/cvm-net"


def test(model=None, data=None):

    if data is None:
        data = load_data(anchor_images_path="/tf/CVUSA/terrestrial",
                         positive_images_path="/tf/CVUSA/satellite",
                         batch_size=BATCH_SIZE)

    # Allows for loading a model in for testing at the end of each epoch
    if model is None:
        print("Loading Model from file ...")
        model = SiameseModel()
        model.load(WEIGHTS_PATH)
        optimiser = optimizers.Adam(0.001)
        model.compile(optimizer=optimiser, weighted_metrics=[])

    # Separate the twins for testing
    gnd_embedding = model.gnd_embedding
    sat_embedding = model.sat_embedding

    # Global descriptors will hold each batch of embeddings temporarily to allow batched predictions
    global_sat_descriptors = []             # [ [e_1, e_2, ... e_n], [e_1, e_2 ... e_n] ]
    global_gnd_descriptors = []             # where e = embedding vector and n = batch_size

    total_steps = data.__len__()

    for step, (gnd, sat_p, sat_n) in enumerate(data.as_numpy_iterator()):
        progress = int(100 * round((float(step)/ float(total_steps)), 2) / 2)
        print(f"\rValidating: [{progress * '='}>{(50-progress) * ' '}]", end='')

        global_gnd_descriptors.append(gnd_embedding.predict(gnd, verbose=0))
        global_sat_descriptors.append(sat_embedding.predict(sat_p, verbose=0))

    # Concatenate batches together into shape (data_length, vector_dimensions)  i.e. (5000, 256)
    global_gnd_descriptors = np.concatenate(global_gnd_descriptors)
    global_sat_descriptors = np.concatenate(global_sat_descriptors)

    global_distances = np.square(scipy.spatial.distance.cdist(global_gnd_descriptors, global_sat_descriptors))

    results = recall_at_k(global_distances)
    print(f"\ntop   1: {results[0]}\n"
          f"top   5: {results[1]}\n"
          f"top  10: {results[2]}\n"
          f"top  1%: {results[3]}\n"
          f"top  5%: {results[4]}\n"
          f"top 10%: {results[5]}\n")


if __name__ == "__main__":
    test()
