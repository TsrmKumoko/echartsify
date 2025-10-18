from typing import List, Union, Literal
import json
import pandas as pd

class DataLoader:
    def __init__(self, option: dict):
        pass

    def build_source(self) -> str:
        pass

class ArrayLoader(DataLoader):
    def __init__(self, option: dict):
        self._x_data = []
        self._y_data_list = []
        self._y_name_list = []
        self._option = option

    def set_x_data(self, x_data: List[Union[int, float]]):
        self._x_data = [''] + x_data

    def add_y_data(self, y_data: List[Union[int, float]], name: str = '', type: Literal['line', 'bar'] = 'line'):
        self._y_data_list.append([name] + y_data)
        self._y_name_list.append(name)
        self._option['series'].append({
            'type': type,
            'seriesLayoutBy': 'row'
        })

    def build_source(self):
        # 检查 x_data 是否为空
        if not self._x_data:
            raise ValueError('x_data must be set')
        # 检查 y_data_list 是否为空
        if not self._y_data_list:
            raise ValueError('y_data must be set')
        # 检查 y_data_list 中每个元素是否与 x_data 长度一致
        for y in self._y_data_list:
            if len(y) != len(self._x_data):
                raise ValueError(f'y_data length must match x_data length for {y[0]}')
        source = [self._x_data] + self._y_data_list
        return source

class DataFrameLoader(DataLoader):
    def __init__(self, df: pd.DataFrame, option: dict):
        self._df = df
        self._option = option

    def build_source(self):
        cols = self._df.columns.tolist()
        for col in cols[1:]:
            self._option['series'].append({
                'type': 'line',
                'name': col,
                'encode': {
                    'x': cols[0],
                    'y': col
                },
                'symbol': 'none'
            })
        return [cols] + self._df.values.tolist()

# dfl = DataFrameLoader(pd.read_csv('test/data.csv', usecols=['time', '3', '5']).head(10))
# print(dfl.build_source())

class EChartBuilder:
    def __init__(self, width, height=None):
        self._width = width
        self._height = height
        self._option = {
            'legend': {},
            'dataset': {
                'source': []
            },
            'xAxis': {
                'type': 'value',
                'nameLocation': 'center',
                'nameGap': 30
            },
            'yAxis': {
                'type': 'value',
                'nameLocation': 'center',
                'nameGap': 30
            },
            'series': []
        }
        self._data_loader: DataLoader = None

    def set_x_title(self, title: str):
        self._option['xAxis']['name'] = title
        return self

    def set_y_title(self, title: str):
        self._option['yAxis']['name'] = title
        return self

    def set_x_data(self, x_data: List[Union[int, float]]):
        if self._data_loader is None:
            self._data_loader = ArrayLoader(self._option)
        self._data_loader.set_x_data(x_data)
        return self

    def add_y_data(self, y_data: List[Union[int, float]], name: str = '', type: Literal['line', 'bar'] = 'line'):
        if self._data_loader is None:
            self._data_loader = ArrayLoader(self._option)
        self._data_loader.add_y_data(y_data, name, type)
        return self

    def load_dataframe(self, df: pd.DataFrame):
        if self._data_loader is None:
            self._data_loader = DataFrameLoader(df, self._option)
        return self

    def set_y_style(self, name: str):
        return self

    def build(self):
        if self._data_loader is None:
            raise ValueError('Some data must be set')
        dataset_source = self._data_loader.build_source()
        self._option['dataset']['source'] = dataset_source
        
        return json.dumps(
            {
                'option': self._option,
                'width': self._width,
                'height': self._height
            },
            ensure_ascii=False,
            # indent=2
        )

    def export_html(self, path: str = 'chart.html'):
        self.build()
        html=f'''
        <!DOCTYPE html>
        <html lang='en'>
        <head>
            <meta charset='UTF-8'>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <title>Chart</title>
        </head>
        <body>
            <div id='main' style='width: {self._width}px; height: {self._height}px;'></div>
            <script src='https://cdn.jsdelivr.net/npm/echarts@6.0.0/dist/echarts.min.js'></script>
            <script>
                var chart = echarts.init(document.getElementById('main'));
                chart.setOption({json.dumps(self._option, ensure_ascii=False)});
                window.addEventListener('resize', function () {{
                    chart.resize();
                }});
                new ResizeObserver(function() {{
                    chart.resize();
                }}).observe(document.getElementById('main'));
            </script>
        </body>
        </html>
        '''
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    
