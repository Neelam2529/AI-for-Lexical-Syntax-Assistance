import torch
import torch.nn as nn

class SyntaxCorrectionModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim=64, hidden_dim=128, max_seq_length=50):
        super(SyntaxCorrectionModel, self).__init__()
        self.max_seq_length = max_seq_length
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True, bidirectional=True)
        
        # Buggy or Clean?
        self.buggy_classifier = nn.Linear(hidden_dim * 2, 2)
        
        # Where is error?
        self.position_classifier = nn.Linear(hidden_dim * 2, max_seq_length)

    def forward(self, x):
        embedded = self.embedding(x)
        
        # LSTM layer
        lstm_out, (hidden, cell) = self.lstm(embedded)
        
        # Classify
        hidden_cat = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1) 
        buggy_logits = self.buggy_classifier(hidden_cat)
        pos_logits = self.position_classifier(hidden_cat)
        
        return buggy_logits, pos_logits

if __name__ == "__main__":
    # Test model with dummy input
    vocab_sz = 100
    model = SyntaxCorrectionModel(vocab_sz)
    dummy_input = torch.randint(1, vocab_sz, (4, 30)) # batch_size=4, seq_len=30
    buggy, pos = model(dummy_input)
    print("Buggy Logits Shape:", buggy.shape)
    print("Pos Logits Shape:", pos.shape)
