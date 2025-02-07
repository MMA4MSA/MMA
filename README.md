# Mixture of Multimodal Adapters for Sentiment Analysis

This repository contains code of Mixture of Multimodal Adapters for Sentiment Analysis, accepted at 2025 Annual Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics (NAACL 2025).

## Introduction

MMA is a plug-and-play module, which can be flexibly applied to various pre-trained language models and transform these models into a multi-modal model that can handle MSA tasks.


## Usage

1. Download the word-aligned CMU-MOSI dataset from [MMSA](https://github.com/thuiar/MMSA). Download the pre-trained BERT model from [Huggingface](https://huggingface.co/google-bert/bert-base-uncased/tree/main).



2. Start training.

Training on CMU-MOSI:

```
python main.py --dataset mosi --data_path [your MOSI path] --bert_path [your bert path]
```
Training on other dataset and LLM:

coming soon.
## Citation



## Contact 
If you have any question, feel free to contact me through chenkezhou@mail.ustc.edu.cn.
