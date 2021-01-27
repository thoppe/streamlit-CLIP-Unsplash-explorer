from fastapi import FastAPI
import pandas as pd
import numpy as np

app_name = "Unsplash+CLIP image similarity"
__version__ = "1.0.0"


class CLIP:
    def load(self, f_latents="data/img_latents.npy", f_keys="data/img_keys.csv"):
        # Load the pre-computed unsplash latent codes
        self.V = np.load(f_latents)
        self.V /= np.linalg.norm(self.V, ord=2, axis=-1, keepdims=True)

        # Load the mapping of the latent codes to the IDs
        self.keys = pd.read_csv(f_keys)["unsplashID"].values

    def top_match(self, i, top_k=10):
        idx = np.argsort(self.V.dot(self.V[i]))[::-1][1 : top_k + 1]
        return self.keys[idx]


app = FastAPI()

clf = CLIP()
clf.load()


@app.get("/")
def root():
    return {
        "app_name": app_name,
        "version": __version__,
    }


@app.get("/top_match")
def top_match(i: int, top_k: int):
    return clf.top_match(i, top_k).tolist()


if __name__ == "__main__":

    from fastapi.testclient import TestClient

    client = TestClient(app)

    r = client.get("/top_match", params={"i": 17, "top_k": 2})
    print(r.json())
