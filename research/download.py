import gdown
import os

if not os.path.exists("63k-subset-resized.zip"):
    gdown.download(id="1tkMXFHsuCCaLRq_P0fbyj1kFA5nrRe2f")

if not os.path.exists("test.csv"):
    gdown.download(id="1-B_U48ywDf6wXtmeesks1sOfG8vZtKKt")
