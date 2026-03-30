import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset
import pickle

# Ensure we can import from local modules
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(base_dir, 'src'))

from models.tokenizer import CodeTokenizer
from models.model import SyntaxCorrectionModel

def prepare_data(dataset_path, max_seq_length=50):
    df = pd.read_csv(dataset_path)
    
    tokenizer = CodeTokenizer()
    tokenizer.fit(df['code'].tolist())
    
    X = []
    y_buggy = []
    y_pos = []
    
    for _, row in df.iterrows():
        tokens = tokenizer.encode(row['code'])
        # Truncate or pad
        seq_len = len(tokens)
        if seq_len > max_seq_length:
            tokens = tokens[:max_seq_length]
        else:
            tokens = tokens + [0] * (max_seq_length - seq_len)
            
        X.append(tokens)
        is_buggy = row['is_buggy']
        y_buggy.append(is_buggy)
        
        # Simple heuristic for dummy data: if buggy, error is usually at the end of the sequence length
        if is_buggy == 1:
            err_pos = min(seq_len - 1, max_seq_length - 1)
        else:
            err_pos = 0 # Dummy value if not buggy
        y_pos.append(err_pos)
        
    X_tensor = torch.tensor(X, dtype=torch.long)
    y_buggy_tensor = torch.tensor(y_buggy, dtype=torch.long)
    y_pos_tensor = torch.tensor(y_pos, dtype=torch.long)
    
    return X_tensor, y_buggy_tensor, y_pos_tensor, tokenizer

def train_model(dataset_path, epochs=10, max_seq_length=50):
    print("Preparing data...")
    X, y_buggy, y_pos, tokenizer = prepare_data(dataset_path, max_seq_length)
    
    dataset = TensorDataset(X, y_buggy, y_pos)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    vocab_size = len(tokenizer.vocab)
    model = SyntaxCorrectionModel(vocab_size=vocab_size, max_seq_length=max_seq_length)
    
    criterion_buggy = nn.CrossEntropyLoss()
    criterion_pos = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    
    print(f"Starting Training for {epochs} epochs...")
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for batch_x, batch_y_buggy, batch_y_pos in loader:
            optimizer.zero_grad()
            buggy_logits, pos_logits = model(batch_x)
            
            loss_buggy = criterion_buggy(buggy_logits, batch_y_buggy)
            
            # Only compute position loss on actual buggy samples
            buggy_mask = (batch_y_buggy == 1)
            if buggy_mask.any():
                loss_pos = criterion_pos(pos_logits[buggy_mask], batch_y_pos[buggy_mask])
                loss = loss_buggy + loss_pos
            else:
                loss = loss_buggy
                
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            
        print(f"Epoch {epoch+1}/{epochs} | Loss: {total_loss/len(loader):.4f}")
    
    # Save Model Weights and Tokenizer
    models_dir = os.path.dirname(os.path.abspath(__file__))
    weights_path = os.path.join(models_dir, 'model_weights.pth')
    torch.save(model.state_dict(), weights_path)
    
    tokenizer_path = os.path.join(models_dir, 'tokenizer.pkl')
    with open(tokenizer_path, 'wb') as f:
        pickle.dump(tokenizer, f)
        
    print(f"Model saved to {weights_path}")
    print(f"Tokenizer saved to {tokenizer_path}")

if __name__ == "__main__":
    data_path = os.path.join(base_dir, "data", "processed", "dataset.csv")
    train_model(data_path, epochs=60)
