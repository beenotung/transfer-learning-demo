# %%
import torch
import torchvision


# %%
print("is cuda available:", torch.cuda.is_available())


# %%
model = torchvision.models.resnet50()


# %%
model.eval()


# %%
import urllib
url = "https://github.com/pytorch/hub/raw/master/images/dog.jpg"
filename = "dog.jpg"
try: urllib.URLopener().retrieve(url, filename)
except: urllib.request.urlretrieve(url, filename)


# %%
from PIL import Image
from torchvision import transforms
input_image = Image.open(filename)
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
input_tensor = preprocess(input_image)
input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

# move the input and model to GPU for speed if available
if torch.cuda.is_available():
    input_batch = input_batch.to('cuda')
    model.to('cuda')

with torch.no_grad():
    output = model(input_batch)
# Tensor of shape 1000, with confidence scores over ImageNet's 1000 classes
# print(output[0])
idx_max = torch.argmax(output[0])
print("argmax(output[0]):", idx_max)
print("value:", output[0][idx_max])
# The output has unnormalized scores. To get probabilities, you can run a softmax on it.
probabilities = torch.nn.functional.softmax(output[0], dim=0)
# print(probabilities)
print("probabilities:",probabilities[idx_max])