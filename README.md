# 塔可夫实时地图工具（仅为开发者提供思路，此分支可能不能正常运行）

为代码添加注释，让他更容易被开发者理解

附上经过初步实验对坐标的初步判断

2024-01-26[19-23]_525.2, 2.6, -106.4_-0.1, 0.1, 0.0, -1.0_10.69 (0)

‘_’ 是对数据的分隔符他将数据分为四部分

第一部分为标准时间戳2024-01-26[19-23]表示精确时间

第二部分25.2, 2.6, -106.4

第二部分又分为三部分 即为 x，z，y，即 左右，高度，上下

第三部分-0.1, 0.1, 0.0可能为非典型四元数，常用于表示三维空间中的旋转，估计是镜头方向 但是没有网站实现这个，可能是没看出来

第四部分 10.69可能是人物角度即方向

（0）含义未知 不过应该不重要，所有信息都已知了
