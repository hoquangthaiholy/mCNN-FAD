
<h1 align="center"><i>m</i>CNN-FAD</h1>
<p align="center"><a href="https://github.com/hoquangthaiholy/mCNN-FAD/blob/master/mCNN_FAD_Identification_of_FAD_binding_sites_in_electron_transport_proteins_using_multiple_windows_scanning_techniques_and_convolutional_neural_networks.ipynb" align="center"><strong>Run <i>m</i>CNN-FAD on Colab »</strong></a></p>
<h2 align="center">
  Using multiple windows scanning techniques and convolutional neural networks to identify FAD binding sites within transport proteins
</h2>

![Figure 1](https://raw.githubusercontent.com/hoquangthaiholy/mCNN-FAD/master/fig_01.png?raw=true)

## Introduction

<p>As we all know, CNN has an excellent ability to distinguish image patterns. It can recognize some patterns in images, such as bird's beak and cat's beard, and use these patterns to help identify what kind of images are. Our goal is to use this pattern recognition capability to predict the functional binding positions of protein sequences with multiple sequence alignment data. The multiple sequence alignment data is slightly different from the image data, but we can regard it as a special one-dimensional image with 20 channels. We use multiple different window sizes to scan multiple sequence alignment matrices of adjacent amino acids at a specific position and generate multiple filters for each window size. We hope to capture some significant patterns from these filters to predict whether an amino acid position will bind to flavin adenine dinucleotide or not.</p>

![Figure 1](https://raw.githubusercontent.com/hoquangthaiholy/mCNN-FAD/master/fig_02.png?raw=true)

<p>Flavin adenine dinucleotide (FAD) is synthesized from riboflavin (vitamin B2) and two molecules of ATP, and FAD plays an important role as a hydrogen carrier and a redox reaction that takes place in more than 100 redox reactions in energy metabolism. Identifying the FAD binding sites in transporters and electron transporters is important because it can help biological researchers understand exactly how these energy metabolism mechanisms work.</p>

![Figure 3](https://raw.githubusercontent.com/hoquangthaiholy/mCNN-FAD/master/fig_03.png?raw=true)

<p>We propose a new method based on multiple window scanning technology and convolutional neural networks to predict FAD-binding sites from transporters and electron transport proteins. The method we proposed successfully classified FAD-binding sites in transporters and electron transporters and achieved satisfactory results. For FAD-binding sites prediction in transporters, the sensitivity (SN), specificity (SP), accuracy (ACC), and Matthews correlation coefficient (MCC) are 87.35%, 91.50%, 91.36%, and 0.4470, respectively. Similarly, it shows 86.50% SN, 81.04% SP, 81.21% ACC and 0.2894 MCC for FAD-binding site identification on electron transport proteins. In addition, we visualized the filters as a sequence logo that is familiar to biologists, and the significant sequence motifs may be used to interpret some interesting patterns of functional binding sites from the field of biology in the future.</p>

![Figure 4](https://raw.githubusercontent.com/hoquangthaiholy/mCNN-FAD/master/fig_04.png?raw=true)

## Publication
The manuscript of this website is under review and not published yet.

## Contact Information

For help or issues using mCNN-FAD, please submit a GitHub issue.

For personal communication related to mCNN-FAD, please contact Yu-Yen Ou
(`yien@saturn.yzu.edu.tw`), Quang-Thai Ho (`hoquangthaiholy@gmail.com`), or
Syed Muazzam Ali Shah (`muazzam.ali72@gmail.com `).

<br/>

![Figure 1](https://raw.githubusercontent.com/hoquangthaiholy/mCNN-FAD/master/yzu.png?raw=true)

<p>
Department of Computer Science and Engineering<br/>
Graduate Program in Biomedical Informatics<br/>
Bioinformatics Laboratory (R1607B)<br/>
Address: No. 135, Yuandong Road, Chungli City, Taoyuan County, Taiwan R.O.C .32003<br/>
Tel: (03) 463-8800
</p>
