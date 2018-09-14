from pyecharts import Geo

data = [('广州', 45), ('漳州', 135), ('A市', 43), ('郑州', 200), ('商城', 5)]
# geo = Geo("全国主要城市空气质量", "data from pm2.5", **style.init_style)
# geo = Geo("全国主要城市空气质量", "data from pm2.5")

geo = Geo("全国主要城市空气质量", "data from pm2.5", title_color="#fff",
          title_pos="center", width=800,
          height=400, background_color='#404a59')
attr, value = geo.cast(data)
geo.add_coordinate("商城", 115.42, 31.81)  # 数据仅供示例/
geo.add_coordinate('A市', 119.3, 26.08)  # 添加 pyecharts 未提供的城市地理坐标
geo.add(
    "全国主要城市空气质量",
    attr,
    value,
    type="effectScatter",
    is_random=True,
    is_visualmap=True,
    is_piecewise=True,
    # symbol_size=10,
    # maptype='china',
    visual_text_color="#fff",
    pieces=[
        {"min": 0, "max": 50, "label": "0 < x < 50"},
        {"min": 50, "max": 200, "label": "50 < x < 200"},
    ],
    effect_scale=5,
)
geo.render()
