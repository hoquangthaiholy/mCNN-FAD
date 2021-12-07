"""
" Dataset preprocessing
" Handling protein sequence data.
"   Split data into train/test set
"""

from sklearn.model_selection import train_test_split
import os
import re
import pandas as pd
from subprocess import call

BLASTDB_PATH = 'D:/Program/blast/db/nr'
PSSM_LIBRARY = 'E:/PSSMs'

def convert_pssm(fid,seq):
    fas = open('.fasta','w')
    fas.writelines([
        f'>sp|{fid}\n',
        seq
    ])
    fas.close()
    print(f'Converting {fid}')
    call(f"blastpgp -i .fasta -a 4 -j 2 -d {BLASTDB_PATH} -Q {PSSM_LIBRARY}/{fid}.pssm", shell=True)
    os.unlink('.fasta')

def read_pssm(fid, maxseq = None):
    arr = []
    j = 0
    if os.path.exists(f"{PSSM_LIBRARY}/{fid}.pssm"):
        pssm = open(f"{PSSM_LIBRARY}/{fid}.pssm").readlines()[3:-6]
        for line in pssm:
            j += 1
            arr.append([float(k) for k in line.split()[2:22]])
        if maxseq != None:
            for c in range(j, maxseq):
                arr.append([0]*20)
    return arr

def uniprot_to_dataframe(file_path, clust_file='', bind = 'FAD'):
    inc_list = []
    if not clust_file == '':
        fin = open(clust_file)
        for line in fin:
            inc_list.append(line.split(' ')[0])
    
    n = -1
    df = pd.DataFrame(columns=['ID', 'SEQUENCE', 'LENGTH', 'LABEL', 'ET', 'NSITE', 'PSSM'])
    all_data = re.split(
        r'^\/\/', ''.join(open(file_path).readlines()), flags=re.M)
    for data in all_data[:-1]:
        matches = re.findall(r'^AC   (\w+);', data, flags=re.M)
        fid = matches[0]

        if (not len(inc_list) == 0 and fid not in inc_list):
            continue

        n += 1

        matches = re.split(r"(^SQ   .*)", data, flags=re.M)
        seq = ''.join(matches[2].split())

        nlen = len(seq)
        labels = ['0']*nlen
        nsite = 0

        et = 0
        matches = re.findall(
            rf'^KW(.*)Electron transport;', data, flags=re.M)
        et = 1 if len(matches)>0 else 0

        matches = re.findall(rf'^FT   NP_BIND         (.*)\nFT                   \/note="{re.escape(bind)}',data, flags=re.M)
        # print(matches)
        for match in matches:
            for i in range(int(match.split('..')[0]),int(match.split('..')[1])+1):
                nsite += 1
                labels[i-1] = '1'
    
        matches = re.findall(rf'^FT   BINDING         (.*)\nFT                   \/note="{re.escape(bind)}',data, flags=re.M)
        # print(matches)
        for match in matches:
            nsite += 1
            labels[int(match)-1] = '1'

        label = ''.join(labels)

        pssm = read_pssm(fid)
        
        if len(pssm) == 0:
            convert_pssm(fid,seq)
            pssm = read_pssm(fid)

        df.loc[n] = [fid, seq, nlen, label, et, nsite, pssm]
    return df

df = uniprot_to_dataframe('uniprot/fad.txt', 'uniprot/fad.30.out', 'FAD')
# df.reset_index(drop=True)
# nad_df = uniprot_to_dataframe('uniprot/nad.txt', 'uniprot/nad.30.out', 'NAD')
# atp_df = uniprot_to_dataframe('uniprot/atp.txt', 'uniprot/atp.30.out', 'ATP')
# fmn_df = uniprot_to_dataframe('uniprot/fmn.txt', 'uniprot/fmn.30.out', 'FMN')

df_tp = df[df.ET == 0]
df_et = df[df.ET == 1]

df_tp = df_tp.reset_index(drop=True)
df_et = df_et.reset_index(drop=True)

# Split validation/test
X_train, X_test, y_train, y_test = train_test_split(
    df_tp[['ID']], df_tp[['ID']], test_size=0.107, random_state=42)

df_train = df_tp.iloc[y_train.index]
df_test  = df_tp.iloc[y_test.index]

df_train = df_train.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)


"""""
" Export PSSM
"
"""
WINDOW_SIZE = 9

def export_csv(df, outfile=''):
    fout = open(outfile, 'w')
    flog = open(f'{outfile}.log', 'w')

    npos = 0
    nneg = 0
    for index, row in df.iterrows():

        pssm = []

        # zero-padding begin
        for c in range(0, (WINDOW_SIZE // 2)):
            pssm.append([0]*20)

        pssm.extend(row.PSSM)

        # zero-padding end
        for c in range(0, (WINDOW_SIZE // 2)):
            pssm.append([0]*20)

        n = len(row.SEQUENCE)
        # print(len(pssm))

        for j in range(0, n):
            # feature = [y for x in pssm[j:j+WINDOW_SIZE] for y in x]
            feature = pssm[j:j+WINDOW_SIZE]
            # print(feature)
            # if (len(feature) < WINDOW_SIZE):
            #     print(df.iloc[i, :].ID, len(feature))
            _feature = []
            for line in feature:
                _feature.extend(line)

            _feature.append(row.LABEL[j])

            if row.LABEL[j] == '1':
                npos += 1
            else:
                nneg += 1

            fout.write(
                f"{','.join(str(x) for x in _feature)}\n")
        # print(row)
        # break
    flog.write(f'Positive: {npos}; Negative: {nneg}')
    fout.close()

export_csv(df_train, f'datasets/fad_w{WINDOW_SIZE}_train.csv')
export_csv(df_test, f'datasets/fad_w{WINDOW_SIZE}_test.csv')
export_csv(df_et, f'datasets/fad_w{WINDOW_SIZE}_et.csv')

# # Split Cross-Validation
# from sklearn.model_selection import KFold
# kf = KFold(n_splits=5) # Define the split - into 2 folds 
# kf.get_n_splits(X_train) # returns the number of splitting iterations in the cross-validator

# print(kf)
# idx = 0
# for train_index, test_index in kf.split(X_train):
#     idx = idx + 1
#     export_csv(df_train.loc[train_index], f'datasets/fad_cv{idx}_w{WINDOW_SIZE}_train.csv')
#     export_csv(df_train.loc[test_index], f'datasets/fad_cv{idx}_w{WINDOW_SIZE}_test.csv')
