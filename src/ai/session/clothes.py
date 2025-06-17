from torchvision.transforms import Compose, Resize, ToTensor
import torch

session = torch.jit.load(
    "src/ai/torchscript/clothes.torchscript")

input_shape = (640, 640)

transformation = Compose([Resize(input_shape), ToTensor()])

labels = [
  'jacket',
  'short pants',
  'tailored pants',
  'jumper',
  'shirts',
  'coat',
  'dress',
  'casual pants',
  'blouse',
  'tshirts',
  'skirt',
  'tearing',
  'pollution',
]
