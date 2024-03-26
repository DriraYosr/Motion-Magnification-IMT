# Motion_magnification_learning-based
This is an unofficial implementation of "[Learning-based Video Motion Magnification](https://arxiv.org/abs/1804.02684)" in Pytorch (1.8.1~2.0).
[Here is the official implementation in Tensorflow==1.8.0](https://github.com/12dmodel/deep_motion_mag).

*Given the video, and amplify it with only one click for all steps:*

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1inOucehJXUAVBlRhZvo650SoOPLKQFNv#scrollTo=BjgKRohk7Q5M)

<p align="center">
<img width="768" alt="VMM_colab_demo" src="https://user-images.githubusercontent.com/25921713/230589573-68d65731-ff7a-4b34-9aa3-e29b4dc6db4b.png">
</p>

# Env
`conda install pytorch==2.0.0 torchvision==0.15.1 pytorch-cuda=11.8 -c pytorch -c nvidia`

`pip install -r requirements.txt`

# Data preparation

Synthetic dataset for **training**: official repository [here](https://drive.google.com/drive/folders/19K09QLouiV5N84wZiTPUMdoH9-UYqZrX?usp=sharing).

1. About the video datasets for **validation**, you can also download the preprocessed frames [here](https://drive.google.com/drive/folders/19K09QLouiV5N84wZiTPUMdoH9-UYqZrX?usp=sharing), which is named train_vid_frames.zip.

The images in the dataset given has 4 parts:

1. frameA:  <img src="https://latex.codecogs.com/svg.latex?X_a" /> , unperturbed;
2. frameB: perturbed frameC, is actually   <img src="https://latex.codecogs.com/svg.latex?X_{b}^{'}" />  in the paper,
3. frameC: the real   <img src="https://latex.codecogs.com/svg.latex?X_b" /> , unperturbed;
4. **amplified**: represent both   <img src="https://latex.codecogs.com/svg.latex?Y" />  and   <img src="https://latex.codecogs.com/svg.latex?Y^{'}" /> , perturbed.

# Run
`bash run.sh` to train and test.

# Results

Here are some results generated from the model trained on the whole synthetic dataset for **12** epochs. 

Baby, amplification factor = 50

![baby](materials/baby_comp.gif)

Guitar, amplification factor = 20

![guitar](materials/guitar_comp.gif)
