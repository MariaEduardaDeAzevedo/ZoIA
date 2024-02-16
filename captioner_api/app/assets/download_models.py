import gdown
url = "https://drive.google.com/drive/folders/1mgbLfXWzCn0IFt4EUzcpzBZrjl2L9lTu?usp=sharing"
print(gdown.download_folder(id="1mgbLfXWzCn0IFt4EUzcpzBZrjl2L9lTu", quiet=True, output="."))
