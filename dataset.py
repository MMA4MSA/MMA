'''
* @name: dataset.py
* @description: Dataset loading functions. Note: The code source references MMSA (https://github.com/thuiar/MMSA/tree/master).
'''


import logging
import pickle
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader


__all__ = ['MMDataLoader']

logger = logging.getLogger('MSA')


class MMDataset(Dataset):
    def __init__(self, args, mode='train'):
        self.mode = mode
        self.args = args
        DATA_MAP = {
            'mosi': self.__init_mosi,
            'mosei': self.__init_mosei,
            'sims': self.__init_sims
        }
        DATA_MAP[args.dataset]()

    def __init_mosi(self):
        path = self.args.data_path
        with open(path, 'rb') as f:
            data = pickle.load(f)

        # self.args.use_bert = True
        # self.args.need_truncated = True
        # self.args.need_data_aligned = True

        # if self.args.use_bert:
        self.text = data[self.mode]['text_bert'].astype(np.float32)
        # else:
            # self.text = data[self.mode]['text'].astype(np.float32)
     
        self.vision = data[self.mode]['vision'].astype(np.float32)
        self.audio = data[self.mode]['audio'].astype(np.float32)

        self.rawText = data[self.mode]['raw_text']
        self.ids = data[self.mode]['id']
        self.labels = {
            'M': data[self.mode]['regression'+'_labels'].astype(np.float32)
        }
        if self.args.dataset == 'sims':
            for m in "TAV":
                self.labels[m] = data[self.mode]['regression'+'_labels_'+m]

        logger.info(f"{self.mode} samples: {self.labels['M'].shape}")

        # if not self.args.need_data_aligned:
            # self.audio_lengths = data[self.mode]['audio_lengths']
            # self.vision_lengths = data[self.mode]['vision_lengths']
        self.audio[self.audio == -np.inf] = 0

        # if self.args.need_truncated:
        #     self.__truncated()

    def __init_mosei(self):
        return self.__init_mosi()

    def __init_sims(self):
        return self.__init_mosi()

    def __len__(self):
        return len(self.labels['M'])

    def get_seq_len(self):
        if self.args.use_bert:
            return (self.text.shape[2], self.audio.shape[1], self.vision.shape[1])
        else:
            return (self.text.shape[1], self.audio.shape[1], self.vision.shape[1])

    def get_feature_dim(self):
        return self.text.shape[2], self.audio.shape[2], self.vision.shape[2]

    def __getitem__(self, index):
        sample = {
            'raw_text': self.rawText[index].lower(),
            'text': torch.Tensor(self.text[index]), 
            'audio': torch.Tensor(self.audio[index]),
            'vision': torch.Tensor(self.vision[index]),
            'index': index,
            'id': self.ids[index],
            'labels': {k: torch.Tensor(v[index].reshape(-1)) for k, v in self.labels.items()}
        } 
        return sample


def MMDataLoader(args):
    datasets = {
        'train': MMDataset(args, mode='train'),
        'valid': MMDataset(args, mode='valid'),
        'test': MMDataset(args, mode='test')
    }

    if 'seq_lens' in args:
        args.seq_lens = datasets['train'].get_seq_len() 

    dataLoader = {
        ds: DataLoader(datasets[ds],
                       batch_size=args.batch_size,
                    #    num_workers=args.num_workers,
                       shuffle=True,
                       generator=torch.Generator(device='cuda'))
        for ds in datasets.keys()
    }
    
    return dataLoader
