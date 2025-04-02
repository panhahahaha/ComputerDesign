import numpy as np
def pixel_to_world(u, v, depth, K=np.array([]), R=None, T=None):
    """
    将像素坐标 (u, v) 转换为世界坐标 (Xw, Yw, Zw)

    参数：
    - u, v: 像素坐标
    - depth: 该像素点的深度值（单位与相机标定一致）
    - K: 3x3 相机内参矩阵
    - R: 3x3 旋转矩阵（如果需要转换到世界坐标）
    - T: 3x1 平移向量（如果需要转换到世界坐标）

    返回：
    - 世界坐标 (Xw, Yw, Zw) 或相机坐标 (Xc, Yc, Zc)
    """

    # 计算归一化坐标 (Xc, Yc, Zc)
    fx, fy = K[0, 0], K[1, 1]  # 焦距
    cx, cy = K[0, 2], K[1, 2]  # 光心坐标

    Xc = (u - cx) * depth / fx
    Yc = (v - cy) * depth / fy
    Zc = depth  # 深度就是 Zc

    camera_coords = np.array([[Xc], [Yc], [Zc]])

    if R is not None and T is not None:
        # 变换到世界坐标系
        world_coords = R @ camera_coords + T
        return world_coords.flatten()  # 返回 (Xw, Yw, Zw)

    return camera_coords.flatten()  # 返回相机坐标 (Xc, Yc, Zc)
