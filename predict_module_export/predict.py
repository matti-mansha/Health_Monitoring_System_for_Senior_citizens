import numpy as np
import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
from torch.nn import Parameter
import math


# Setup device-agnostic code
device = "cuda" if torch.cuda.is_available() else "cpu"
device

class IndRNNCell(nn.Module):
    r"""An IndRNN cell with tanh or ReLU non-linearity.
    .. math::
        h' = \tanh(w_{ih} * x + b_{ih}  +  w_{hh} (*) h)
    With (*) being element-wise vector multiplication.
    If nonlinearity='relu', then ReLU is used in place of tanh.
    Args:
        input_size: The number of expected features in the input x
        hidden_size: The number of features in the hidden state h
        bias: If ``False``, then the layer does not use bias weights b_ih and b_hh.
            Default: ``True``
        nonlinearity: The non-linearity to use ['tanh'|'relu']. Default: 'relu'
        hidden_min_abs: Minimal absolute inital value for hidden weights. Default: 0
        hidden_max_abs: Maximal absolute inital value for hidden weights. Default: None
    Inputs: input, hidden
        - **input** (batch, input_size): tensor containing input features
        - **hidden** (batch, hidden_size): tensor containing the initial hidden
          state for each element in the batch.
    Outputs: h'
        - **h'** (batch, hidden_size): tensor containing the next hidden state
          for each element in the batch
    Attributes:
        weight_ih: the learnable input-hidden weights, of shape
            `(input_size x hidden_size)`
        weight_hh: the learnable hidden-hidden weights, of shape
            `(hidden_size)`
        bias_ih: the learnable input-hidden bias, of shape `(hidden_size)`
    Examples::
        >>> rnn = nn.IndRNNCell(10, 20)
        >>> input = Variable(torch.randn(6, 3, 10))
        >>> hx = Variable(torch.randn(3, 20))
        >>> output = []
        >>> for i in range(6):
        ...     hx = rnn(input[i], hx)
        ...     output.append(hx)
    """

    def __init__(self, input_size, hidden_size, bias=True, nonlinearity="relu",
                 hidden_min_abs=0, hidden_max_abs=None):
        super(IndRNNCell, self).__init__()
        self.hidden_max_abs = hidden_max_abs
        self.hidden_min_abs = hidden_min_abs
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.bias = bias
        self.nonlinearity = nonlinearity
        self.weight_ih = Parameter(torch.Tensor(hidden_size, input_size))
        self.weight_hh = Parameter(torch.Tensor(hidden_size))
        if bias:
            self.bias_ih = Parameter(torch.Tensor(hidden_size))
        else:
            self.register_parameter('bias_ih', None)
        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1.0 / math.sqrt(self.hidden_size)
        for name, weight in self.named_parameters():
            if "bias" in name:
                weight.data.zero_()
            elif "weight_hh" in name:
                if self.hidden_max_abs:
                    stdv_ = self.hidden_max_abs
                else:
                    stdv_ = stdv
                weight.data.uniform_(-stdv_, stdv_)
            elif "weight_ih" in name:
                weight.data.normal_(0, 0.01)
            else:
                weight.data.normal_(0, 0.01)
                # weight.data.uniform_(-stdv, stdv)
        self.check_bounds()

    def check_bounds(self):
        if self.hidden_min_abs:
            abs_kernel = torch.abs(self.weight_hh.data)
            min_abs_kernel = torch.clamp(abs_kernel, min=self.hidden_min_abs)
            self.weight_hh.data.copy_(
                torch.mul(torch.sign(self.weight_hh.data), min_abs_kernel))
        if self.hidden_max_abs:
            self.weight_hh.data.copy_(
                torch.clamp(self.weight_hh.data, max=self.hidden_max_abs,
                            min=-self.hidden_max_abs))

    def forward(self, input, hx):
        if self.nonlinearity == "tanh":
            func = IndRNNTanhCell
        elif self.nonlinearity == "relu":
            func = IndRNNReLuCell
        else:
            raise RuntimeError(
                "Unknown nonlinearity: {}".format(self.nonlinearity))

        return func(input, hx, self.weight_ih, self.weight_hh, self.bias_ih)


def IndRNNTanhCell(input, hidden, w_ih, w_hh, b_ih=None):
    hy = F.tanh(F.linear(input, w_ih, b_ih) + F.mul(w_hh, hidden))
    return hy


def IndRNNReLuCell(input, hidden, w_ih, w_hh, b_ih=None):
    # hy = F.relu(F.linear(input, w_ih, b_ih) + F.mul(w_hh, hidden))
    # print(input.dtype)
    # print(hidden.dtype)
    # print(w_ih.dtype)
    # print(w_hh.dtype)
    # print(b_ih.dtype)


    hy = F.relu(F.linear(input, w_ih, b_ih) + torch.mul(w_hh, hidden))
    return hy


class IndRNN(nn.Module):
    r"""Applies a multi-layer IndRNN with `tanh` or `ReLU` non-linearity to an
    input sequence.
    For each element in the input sequence, each layer computes the following
    function:
    .. math::
        h_t = \tanh(w_{ih} x_t + b_{ih}  +  w_{hh} (*) h_{(t-1)})
    where :math:`h_t` is the hidden state at time `t`, and :math:`x_t` is
    the hidden state of the previous layer at time `t` or :math:`input_t`
    for the first layer. (*) is element-wise multiplication.
    If :attr:`nonlinearity`='relu', then `ReLU` is used instead of `tanh`.
    Args:
        input_size: The number of expected features in the input `x`
        hidden_size: The number of features in the hidden state `h`
        num_layers: Number of recurrent layers.
        nonlinearity: The non-linearity to use. Can be either 'tanh' or 'relu'. Default: 'tanh'
        bias: If ``False``, then the layer does not use bias weights `b_ih` and `b_hh`.
            Default: ``True``
        batch_first: If ``True``, then the input and output tensors are provided
            as `(batch, seq, feature)`
    Inputs: input, h_0
        - **input** of shape `(seq_len, batch, input_size)`: tensor containing the features
          of the input sequence. The input can also be a packed variable length
          sequence. See :func:`torch.nn.utils.rnn.pack_padded_sequence`
          or :func:`torch.nn.utils.rnn.pack_sequence`
          for details.
        - **h_0** of shape `(num_layers * num_directions, batch, hidden_size)`: tensor
          containing the initial hidden state for each element in the batch.
          Defaults to zero if not provided.
    Outputs: output, h_n
        - **output** of shape `(seq_len, batch, hidden_size * num_directions)`: tensor
          containing the output features (`h_k`) from the last layer of the RNN,
          for each `k`.  If a :class:`torch.nn.utils.rnn.PackedSequence` has
          been given as the input, the output will also be a packed sequence.
        - **h_n** (num_layers * num_directions, batch, hidden_size): tensor
          containing the hidden state for `k = seq_len`.
    Attributes:
        cells[k]: individual IndRNNCells containing the weights
    Examples::
        >>> rnn = nn.IndRNN(10, 20, 2)
        >>> input = torch.randn(5, 3, 10)
        >>> h0 = torch.randn(2, 3, 20)
        >>> output = rnn(input, h0)
    """

    def __init__(self, input_size, hidden_size, n_layer=1, batch_norm=False,
                 step_size=None, **kwargs):
        super(IndRNN, self).__init__()
        self.hidden_size = hidden_size
        if batch_norm and step_size is None:
            raise Exception("Frame wise batch size needs to know the step size")
        self.batch_norm = batch_norm
        self.step_size = step_size
        self.n_layer = n_layer

        cells = []
        for i in range(n_layer):
            if i == 0:
                cells += [IndRNNCell(input_size, hidden_size, **kwargs)]
            else:
                cells += [IndRNNCell(hidden_size, hidden_size, **kwargs)]
        self.cells = nn.ModuleList(cells)

        if batch_norm:
            bns = []
            for i in range(n_layer):
                bns += [nn.BatchNorm2d(step_size)]
            self.bns = nn.ModuleList(bns)

        h0 = torch.zeros(hidden_size)
        self.register_buffer('h0', torch.autograd.Variable(h0))

    def forward(self, x, hidden=None):

        for i, cell in enumerate(self.cells):
            cell.check_bounds()
            hx = self.h0.unsqueeze(0).expand(x.size(0), self.hidden_size).contiguous()
            outputs = []
            for t in range(x.size(1)):
                x_t = x[:, t]
                hx = cell(x_t, hx)
                outputs += [hx]
            x = torch.stack(outputs, 1)
            if self.batch_norm:
                x = self.bns[i](x)
        return x.squeeze(2)


torch.manual_seed(1)

class BaseModel(nn.Module):

    def __init__(self, inputDim, hiddenNum, outputDim, layerNum, cell):

        super(BaseModel, self).__init__()
        self.hiddenNum = hiddenNum
        self.inputDim = inputDim
        self.outputDim = outputDim
        self.layerNum = layerNum

        if cell == "INDRNN":
            self.cell = IndRNN(input_size=self.inputDim, hidden_size=self.hiddenNum, n_layer= self.layerNum)
        print("cell type:", self.cell)
        self.fc = nn.Linear(self.hiddenNum, self.outputDim)


class IndRNNModel(BaseModel):

    def __init__(self, inputDim, hiddenNum, outputDim, layerNum):
        super(IndRNNModel, self).__init__(inputDim, hiddenNum, outputDim, layerNum, cell="INDRNN")

    def forward(self, x, batchSize):

        #h0 = torch.zeros(self.layerNum*1, batchSize, 28)

        rnnOutput = self.cell(x,)

        rnnOutput = rnnOutput[:, -1, :].squeeze()

        out = self.fc(rnnOutput)
        # out = F.log_softmax(out)
        out = F.log_softmax(out, dim=1)


        return out


def extract_key_frames(data):
    # Initialize an empty list to store the key frames
    key_frames = []

    # Calculate the difference between consecutive frames
    frame_diff = np.diff(data, axis=0)

    # Calculate the Euclidean distance between consecutive frames
    frame_dist = np.linalg.norm(frame_diff, axis=1)

    # Set a threshold for motion change
    motion_threshold = 0.05

    # Iterate over the frames and check for key frames
    for i in range(len(frame_dist)):
        if np.any(frame_dist[i] > motion_threshold):
            # If any element in frame_dist[i] exceeds the threshold, add the frame as a key frame
            key_frames.append(data[i])

    # Convert the key frames list to a NumPy array
    key_frames = np.array(key_frames)
        
    # print(key_frames.shape[0])
    if key_frames.shape[0] >= 20:
      # Calculate the equi-distance between the key frames.
      key_frame_interval = len(key_frames) // 20

      # Get the indices of the equi-distance key frames.
      equi_distance_key_frame_indices = np.arange(0, len(key_frames), key_frame_interval)

      # Return the equi-distance key frames.
      return key_frames[equi_distance_key_frame_indices]
    else:
    # Return the subset of key frames
      return np.array([])

model = IndRNNModel(inputDim=60, hiddenNum=256, outputDim=3, layerNum=3)
model.load_state_dict(torch.load('model_v2.pth', map_location=torch.device('cpu')))


def predict_function(input_data, model=model):
    model.eval()
    # print(type(input_data))
    # print(input_data.shape)

    x = input_data[:20]
    # input_data = extract_key_frames(input_data)
    # print(type(x))
    # print(x.shape)
    x = torch.from_numpy(x)
    x = Variable(x)
    x = x.view(-1, 20, 60)
    # print(x.shape)
    x = x.squeeze()
    x = x.reshape(60, 20)

    with torch.no_grad():
        # output = model(input_data.unsqueeze(0))
        predictions = model(x.float(), 1)
        _, predicted = torch.max(predictions, dim=1)

    return predicted
