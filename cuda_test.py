import torch

cuda_available = torch.cuda.is_available()
print(f"CUDA is available: {cuda_available}")