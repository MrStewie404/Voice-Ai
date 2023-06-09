import os
os.system('cls')
os.system("echo Загружено OS")
from transformers import GPT2LMHeadModel, GPT2Tokenizer
os.system("echo Загружено TRANSFORMERS")
import torch
os.system("echo Загружено TORCH")
import time
os.system("echo Загружено TIME")
import json

# Загрузка предобученной модели и токенизатора
model_name='sberbank-ai/rugpt3medium_based_on_gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)#.cuda()
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

os.system("echo Загружено GPT-2")

def generate_text(text):
	with open(f'config.json', 'r') as f:
		config = json.load(f)
		max_length = config['max_length']
		temperature = config['temperature']
		top_k = config['top_k']
		top_p = config['top_p']
		repetition_penalty = config['repetition_penalty']
		length_penalty = config['length_penalty']
		no_repeat_ngram_size = config['no_repeat_ngram_size']
		num_beams = config['num_beams']
	input_str = str(text)
	tokenizer.add_special_tokens({'pad_token': '[PAD]'})
	encoded_input = tokenizer.encode_plus(input_str, truncation=True, return_tensors='pt')
	generated_output = model.generate(
		input_ids=encoded_input['input_ids'],
		do_sample=True,
		max_length=max_length + len(text)/3,
		top_p=top_p,	
		temperature=temperature,
		repetition_penalty=repetition_penalty,
		length_penalty=length_penalty,
		no_repeat_ngram_size=no_repeat_ngram_size,
		num_beams = num_beams
	)
	response = tokenizer.decode(generated_output[0], skip_special_tokens=True)
	response = response.replace(text, "")
	return response