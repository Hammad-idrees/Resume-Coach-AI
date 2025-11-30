"""
Resume-Job Match Score Prediction Model Training
Fine-tunes DistilBERT for regression task to predict match scores (0-100)
"""

import torch
import pandas as pd
import numpy as np
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from torch.utils.data import Dataset
import os

# Check CUDA availability
print(f"CUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"CUDA Version: {torch.version.cuda}")
else:
    print("WARNING: CUDA not available, training will be slow on CPU")

# Create necessary directories
os.makedirs('models/resume_scorer', exist_ok=True)

class ResumeJobDataset(Dataset):
    """Custom Dataset for resume-job matching"""
    
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.float)
        return item
    
    def __len__(self):
        return len(self.labels)

def load_and_prepare_data(csv_path='data/training_dataset.csv'):
    """Load and preprocess the dataset"""
    print(f"\nLoading data from {csv_path}...")
    
    # Try loading prepared dataset, fallback to sample
    if not os.path.exists(csv_path):
        print(f"⚠️  {csv_path} not found!")
        print("Run 'python prepare_data.py' first to download and prepare Kaggle datasets")
        csv_path = 'data/sample_dataset.csv'
        if not os.path.exists(csv_path):
            raise FileNotFoundError("No dataset found! Please run prepare_data.py first")
    
    df = pd.read_csv(csv_path)
    
    print(f"Dataset size: {len(df)} samples")
    print(f"Match score range: {df['match_score'].min()} - {df['match_score'].max()}")
    
    # Combine resume and job description
    texts = []
    for _, row in df.iterrows():
        combined_text = f"Resume: {row['resume_text']} [SEP] Job: {row['job_description']}"
        texts.append(combined_text)
    
    # Normalize scores to 0-1 range for better training
    labels = df['match_score'].values / 100.0
    
    # Split data
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )
    
    print(f"Training samples: {len(train_texts)}")
    print(f"Validation samples: {len(val_texts)}")
    
    return train_texts, val_texts, train_labels, val_labels

def tokenize_data(tokenizer, texts):
    """Tokenize text data"""
    return tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors='pt'
    )

def compute_metrics(pred):
    """Calculate regression metrics"""
    labels = pred.label_ids
    preds = pred.predictions
    
    # Predictions are logits, squeeze to get single values
    preds = preds.squeeze()
    
    # Clip predictions to valid range
    preds = np.clip(preds, 0, 1)
    
    mse = mean_squared_error(labels, preds)
    mae = mean_absolute_error(labels, preds)
    rmse = np.sqrt(mse)
    
    # Convert back to 0-100 scale for interpretability
    mae_scaled = mae * 100
    rmse_scaled = rmse * 100
    
    return {
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'mae_scaled': mae_scaled,
        'rmse_scaled': rmse_scaled
    }

def main():
    print("="*60)
    print("Resume-Job Match Score Training")
    print("="*60)
    
    # Load tokenizer and model
    print("\nLoading DistilBERT model and tokenizer...")
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    
    # For regression task, num_labels=1
    model = DistilBertForSequenceClassification.from_pretrained(
        'distilbert-base-uncased',
        num_labels=1,
        problem_type="regression"
    )
    
    # Load and prepare data
    train_texts, val_texts, train_labels, val_labels = load_and_prepare_data()
    
    # Tokenize
    print("\nTokenizing data...")
    train_encodings = tokenize_data(tokenizer, train_texts)
    val_encodings = tokenize_data(tokenizer, val_texts)
    
    # Create datasets
    train_dataset = ResumeJobDataset(train_encodings, train_labels)
    val_dataset = ResumeJobDataset(val_encodings, val_labels)
    
    # Training arguments optimized for GPU
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=10,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=200,
        weight_decay=0.02,
        logging_dir='./logs',
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="mae",
        fp16=torch.cuda.is_available(),  # Use mixed precision if GPU available
        learning_rate=1e-5,
        save_total_limit=3,
    )
    
    # Initialize Trainer
    print("\nInitializing Trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )
    
    # Train
    print("\nStarting training...")
    print("This may take 10-30 minutes depending on your GPU...")
    trainer.train()
    
    # Evaluate
    print("\nEvaluating model...")
    eval_results = trainer.evaluate()
    print("\nFinal Evaluation Results:")
    for key, value in eval_results.items():
        print(f"  {key}: {value:.4f}")
    
    # Save model
    print("\nSaving model and tokenizer...")
    model.save_pretrained('./models/resume_scorer')
    tokenizer.save_pretrained('./models/resume_scorer')
    
    print("\n" + "="*60)
    print("✅ Training completed successfully!")
    print(f"✅ Model saved to: ./models/resume_scorer")
    print(f"✅ Mean Absolute Error: {eval_results['eval_mae_scaled']:.2f} points (on 0-100 scale)")
    print("="*60)
    
    # Test with a sample
    print("\nTesting with sample prediction...")
    test_sample()

def test_sample():
    """Test the trained model with a sample"""
    from transformers import pipeline
    
    # Load the saved model
    model = DistilBertForSequenceClassification.from_pretrained('./models/resume_scorer')
    tokenizer = DistilBertTokenizer.from_pretrained('./models/resume_scorer')
    
    # Create pipeline
    device = 0 if torch.cuda.is_available() else -1
    
    # Test sample
    resume = "Python Developer with 5 years experience in Django, FastAPI, and React. Built ML models with PyTorch."
    job = "Seeking Python Developer with FastAPI and ML experience. 3+ years required."
    
    combined = f"Resume: {resume} [SEP] Job: {job}"
    
    # Tokenize and predict
    inputs = tokenizer(combined, return_tensors="pt", truncation=True, max_length=512)
    
    if torch.cuda.is_available():
        model = model.cuda()
        inputs = {k: v.cuda() for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
        score = outputs.logits.item()
        # Clip and scale to 0-100
        score = np.clip(score, 0, 1) * 100
    
    print(f"\nSample Test:")
    print(f"Resume: {resume[:80]}...")
    print(f"Job: {job[:80]}...")
    print(f"Predicted Match Score: {score:.2f}/100")

if __name__ == "__main__":
    main()
