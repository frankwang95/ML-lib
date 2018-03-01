import pandas as pd
from learning_lib.nn.monitoring.base_monitoring import BaseMonitor


class LossMonitor(BaseMonitor):
    def __init__(self, update_interval):
        super().__init__(pd.DataFrame({'epochs': [], 'loss': []}), update_interval)

    def evaluate(self, train_in, train_out):
        loss_val = self.network.session.run(
            self.network.loss_val,
            feed_dict={self.network.input: train_in, self.network.train_targets: train_out}
        )
        self.values = self.values.append(
            {'epochs': self.network.epochs, 'loss': loss_val},
            ignore_index=True
        )

    def plot(self):
        layout = go.Layout(
            title='Model Loss vs. Epochs',
            xaxis=dict(title='Epochs'),
            yaxis=dict(title='Loss')
        )
        data = [
            go.Scatter(
                x=self.values['epochs'],
                y=welf.values['loss']
            )
        ]
        fig = go.Figure(data=data, layout=layout)
        plotly.iplot(fig)
