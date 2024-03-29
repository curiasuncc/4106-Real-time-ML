# -*- coding: utf-8 -*-
"""2_pre_trained_networks w/ptflop.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jOkIJYAQ9VqIyG04HWrPFak1XJYxpHmU
"""

from torchvision import models

dir(models)

alexnet = models.AlexNet()

resnet = models.resnet101(pretrained=True)

resnet

from torchvision import transforms
preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )])

from PIL import Image
img = Image.open("/content/elguit.jpg")

img

img_t = preprocess(img)

import torch
batch_t = torch.unsqueeze(img_t, 0)

resnet.eval()

out = resnet(batch_t)
out

with open('/content/test.txt') as f:
    labels = [line.strip() for line in f.readlines()]

_, index = torch.max(out, 1)

percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
labels[index[0]], percentage[index[0]].item()

_, indices = torch.sort(out, descending=True)
[(labels[idx], percentage[idx].item()) for idx in indices[0][:5]]

!pip install ptflops

#import torchvision.models as models

from ptflops import get_model_complexity_info

#with torch.cuda.device(0):
#net = models.resnet101()
macs, params = get_model_complexity_info(resnet, (3, 224, 224), as_strings=True,
                                           print_per_layer_stat=True, verbose=True)
print('{:<30}  {:<8}'.format('Computational complexity: ', macs))
print('{:<30}  {:<8}'.format('Number of parameters: ', params))