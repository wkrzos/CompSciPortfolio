import torch
print('cuda_available', torch.cuda.is_available())
print('torch_version', torch.__version__)
print('torch_cuda_version', getattr(torch.version, 'cuda', None))
print('device_count', torch.cuda.device_count())
print('device_name_0', (torch.cuda.get_device_name(0) if torch.cuda.is_available() else None))
try:
    t = torch.randn(1, 1000, 1000, device='cuda')
    t2 = t * t
    print('cuda_op_success', t2.shape, t2.device)
except Exception as e:
    print('cuda_op_failed', type(e).__name__, str(e))
    print('fallback_recommended', 'cpu')
