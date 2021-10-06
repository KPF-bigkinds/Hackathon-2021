import torch
from torch.nn import functional as F
from transformers import BertModel


class bbqqClassifer(torch.nn.Module):
    def __init__(self, bert: BertModel, num_class : int):
        super().__init__()
        self.bert = bert
        # self.hidden_size = hidden_size
        self.linear = torch.nn.Linear(self.bert.config.hidden_size, num_class) # (H, 3)

    def forward(self, X: torch.Tensor):
        """
        :param X:
        :return:
        """
        input_ids = X[:, 0]
        token_type_ids = X[:, 1]
        attention_mask = X[:, 2]
        H_all = self.bert(input_ids, token_type_ids, attention_mask)[0]
        return H_all

    def predict(self, X):
        H_all = self.forward(X) # N, L, H
        H_cls = H_all[:, 0, :] # 한개만 가져오니까 N,H
        y_hat = self.linear(H_cls)# N,H  H,3 -> N,3
        y_hat = torch.sigmoid(y_hat)# N,3
        return y_hat #N,3

    def training_step(self, X, y):
        '''
        :param X:
        :param y:
        :return: loss
        '''
        y_pred = self.predict(X)
        # loss
        loss = F.cross_entropy(y_pred, y).sum()
        return loss
