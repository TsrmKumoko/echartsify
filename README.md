# EChartsify

## 使用方法

### 安装

clone 项目到本地后，进入 src 目录，执行以下命令安装依赖：

```bash
pip install -e .
```

安装完成后，就可以在对应的虚拟环境中 `import echartsify` 了。

### 快速上手

声明式构建图表，支持链式调用方法。
通过调用 `build()` 方法返回图表配置。

```python
from echartsify import EChartBuilder

chart = (
	EChartBuilder(600, 400)
	.set_x_title('X Axis')
	.set_y_title('Y Axis')
	.set_x_data([1, 2, 3, 4, 5])
	.add_y_data([1, 3, 1, 2, 4], 'y1')
	.add_y_data([5, 4, 3, 2, 1], 'y2')
	.build()
)
```

### 使用 DataFrame 加载数据

通过调用 `load_dataframe()` 方法加载 DataFrame 数据。第一列为 X 轴数据，其他列为 Y 轴数据。

```python
import pandas as pd
df = pd.read_csv('data.csv')

chart = (
    EChartBuilder(600, 400)
    .set_x_title('X Axis')
    .set_y_title('Y Axis')
    .load_dataframe(df)
    .build()
)
```

### 预览

使用 `export_html()` 方法导出 HTML 文件。

```python
chart = (
    EChartBuilder(600, 400)
    .load_dataframe(df)
    .export_html('chart.html')
)
```

建议使用 VSCode 的 Live Server 插件预览 HTML 文件。当然也可以直接在浏览器中打开 HTML 文件，但需要手动刷新。
