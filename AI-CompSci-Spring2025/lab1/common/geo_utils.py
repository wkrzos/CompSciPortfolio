from math import radians, cos, sin, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on Earth."""
    R = 6371  # Earth radius in km
    phi1, phi2 = radians(lat1), radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)
    
    sin_dphi_2 = sin(delta_phi/2)
    sin_dlambda_2 = sin(delta_lambda/2)
    cos_phi1 = cos(phi1)
    cos_phi2 = cos(phi2)
    
    a = sin_dphi_2**2 + cos_phi1 * cos_phi2 * sin_dlambda_2**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c
