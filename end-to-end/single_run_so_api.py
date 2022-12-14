from models.single_model_so_api import MulaRecSOAPI
from utils import set_logger
from datetime import datetime
import pytz
import logging
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_length", type=int, required=True,
                        help="max length")
    parser.add_argument("--batch_size", type=int, required=True,
                        help="training batch size")
    parser.add_argument("--norm", type=bool, default=False,
                        help="normalize or not")
    parser.add_argument("--output_dir", type=str, required=True,
                        help="output directory") 
    parser.add_argument("--epoch", type=int, default=30,
                        help="training epoch") 
    args = parser.parse_args()
    
    set_logger('./log/single_{}.log'.format(datetime.now(pytz.timezone('Asia/Singapore'))))
    logging.info(args)
    logging.info(f'Training Single SO API Model')
    
    model = MulaRecSOAPI(codebert_path = 'microsoft/codebert-base', 
        decoder_layers = 6,
        fix_encoder = False, 
        beam_size = 5,
        max_source_length = args.max_length,
        max_target_length = args.max_length,
        l2_norm = args.norm,
        load_model_path = None
    )
    
    # train model
    model.train(
        # train_filename ='../data/train_3_lines.csv',
        # train_filename ='../data/train.csv',
        train_filename ='../data/train_sample_10k.csv',
        train_batch_size = args.batch_size, 
        num_train_epochs = args.epoch, 
        learning_rate = 5e-5,
        do_eval = True, 
        # dev_filename ='../data/validate_3_lines.csv', 
        # dev_filename ='../data/valid.csv', 
        dev_filename ='../data/valid_sample_100.csv', 
        eval_batch_size = 32,
        output_dir = args.output_dir
    )