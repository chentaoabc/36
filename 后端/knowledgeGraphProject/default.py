NEIGHBOR_NUM = 20


###莫兰迪色系
NODE_COLOR = {
        # Pink 粉红
        'BPSK': '#8595A4',
        # Crimson 猩红
        'QPSK': '#DC143C',
        # LavenderBlush 脸红的淡紫色
        'OQPSK': '#FFF0F5',
        # HotPink 热情的粉红色
        'DQPSK': '#FF69B4',
        # Orchid 兰花的紫色
        '2ASK': '#DA70D6',
        # Violet 紫罗兰
        '2FSK': '#EE82EE',
        # DarkMagenta 深洋红色
        '16QAM': '#7C8870',
        # DeepPink 深粉色
        '32QAM': '#FF1493',
        # Thistle 	蓟
        '64QAM': '#D8BFD8',
        # MediumVioletRed 适中的紫罗兰红色
        'GMSK': '#C71585',
        # MediumOrchid 适中的兰花紫
        '4CPM': '#BA55D3',
        # MediumSlateBlue 适中的板岩暗蓝灰色
        '窄带干扰': '#7B68EE',
        # DarkSlateBlue 深岩暗蓝灰色
        '宽带干扰': '#483D8B',
        # GhostWhite 幽灵的白色
        '单音干扰': '#F8F8FF',
        # Blue 纯蓝
        '多音干扰': '#0000FF',
        # CornflowerBlue 矢车菊的蓝色
        '噪声干扰': '#6495ED',
        # LightSkyBlue 淡蓝色
        '扫频干扰': '#87CEFA',
        # CadeBlue 军校蓝
        '阻塞式': '#5F9EA0',
        # Cyan 青色
        '瞄准式': '#00FFFF',
        # DarkSlateGray 深石板灰
        '梳妆': '#2F4F4F'
}

LINE_STYLE = {
        'signal_with_signal': {
                # Lime 酸橙色
                'color': '#00FF00',
                'type': 'dotted',
                # 'width': 5,
                # 'curveness': 0.15,
                'width': 2,
                'curveness': 0.15,


        },
        'signal_with_noise': {
                # Gray 灰色
                'color': '#2E8B57',
                'type':'groove',
                'width': 2,
                # 'curveness': 0.2,



        },
        'noise_with_noise': {
                # Yellow 黄色
                'color': '#FFFF00',
                'type': 'dotted',
                # 'width': 4,
                # 'curveness': 0.1,
                'width': 2,
                'curveness': 0.1,

        }
}
