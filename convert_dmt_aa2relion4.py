#/usr/bin/python3
# Convert the entire cilia from AA to dynamo

import numpy as np
import pandas as pd

from eulerangles import euler2matrix
from eulerangles import matrix2euler
from eulerangles import euler2euler
from eulerangles import convert_eulers

def write_star_4(dfin, outfile):
    out = open(outfile, 'w')
    out.write("# version 30001 from aa\n\n")
    out.write("data_particles\n\n")
    out.write("loop_\n")
    for i in range(len(dfin.columns)):
        out.write('_rln{:s} #{:d}\n'.format(dfin.columns[i], i+1))
    out.write(dfin.to_string(index=False, header=False))
    out.write("\n")
    out.close()		


"""Convert aa doc & star to dynamo table"""
def aa_to_relion(starFile, docFile, TomoName, tomoNo, binFactor, pixelSize, doubletId):
    # Read the doc file
    header_list=["no", "norec", "phi", "theta", "psi", "OriginX", "OriginY", "OriginZ", "cc"]
    df = pd.read_csv(docFile, delim_whitespace=True, names=header_list)
    fulldata = df.to_numpy()

    # Extract phi, theta, psi (AA format) and reverse sign of phi & psi
    eulers_zyz = fulldata[:, 2:5]*-1
    eulers_zyz[:,1] = eulers_zyz[:,1]*-1

    eulers_dynamo = euler2euler(eulers_zyz, source_axes='zyz', source_intrinsic=True, source_right_handed_rotation=True,
                                target_axes='zxz', target_intrinsic=True,target_right_handed_rotation=True,invert_matrix=False)

    # Read the star file (ignore header for now)
    star_header = ["no", "c2", "c3", "c4", "CoordinateX", "CoordinateY", "CoordinateZ", "c8", "c9", "c10", "c11", "c12", "c13", "c14", "c15", "c16"]
    df2 = pd.read_csv(starFile, delim_whitespace=True, names=star_header)
    fullstar = df2.to_numpy()

    # Extract origin
    origin = fullstar[:, 4:7]
    nrows, ncols = origin.shape

    # Hard Code Here


    header_list = ["TomoName", "TomoParticleId", "TomoManifoldIndex", "CoordinateX", "CoordinateY", "CoordinateZ", "OriginXAngst", "OriginYAngst", "OriginZAngst", "AngleRot", "AngleTilt", "AnglePsi", "ClassNumber", "RandomSubset"]
    df_relion = pd.DataFrame(columns = header_list)
    df_relion['TomoParticleId'] = np.arange(len(df2), dtype=np.int16) + 1
    df_relion['TomoManifoldIndex'] = np.ones(len(df2['CoordinateX']), dtype=np.int16)*doubletId	
    df_relion['CoordinateX'] = df2['CoordinateX']*binFactor;
    df_relion['CoordinateY'] = df2['CoordinateY']*binFactor;
    df_relion['CoordinateZ'] = df2['CoordinateZ']*binFactor;

    df_relion['OriginXAngst'] = np.zeros(len(df_relion['CoordinateX']))
    df_relion['OriginYAngst'] = np.zeros(len(df_relion['CoordinateX']))
    df_relion['OriginZAngst'] = np.zeros(len(df_relion['CoordinateX']))

    # Reset angle for debug
    eulers_relion = convert_eulers(eulers_dynamo, source_meta='dynamo', target_meta='warp')
    df_relion['AngleRot'] = eulers_relion[:,0]
    df_relion['AngleTilt'] = eulers_relion[:,1]
    df_relion['AnglePsi'] = eulers_relion[:,2]


    df_relion['ClassNumber'] = np.ones(len(df_relion['CoordinateX']), dtype=np.int8)

    for i in range(len(df2['CoordinateX'])):
        df_relion.loc[i, ('TomoName')] = tomoName

    a = np.empty((len(df_relion['CoordinateX']),), dtype=np.int8)
    a[::2] = 1
    a[1::2] = 2

    df_relion['RandomSubset'] = a
    
    return df_relion


if __name__=='__main__':
    tomoList = ["TS_41", "TS_43", "TS_46", "TS_47"]
    tomoNo = 1;
    pixelSize = 8.48
    binFactor = 4
    df_all = None
    for tomoName in tomoList:
        print(tomoName)
        #for doubletId in range(1,10):
        for doubletId in range(1,10):
            print('-->' + str(doubletId))
            starFile = 'star/' + tomoName + '_' + str(doubletId) + '.txt'
            docFile = 'doc/doc_total_' + tomoName + '_00' + str(doubletId) + '.spi'
            df_relion = aa_to_relion(starFile, docFile, tomoName, tomoNo, binFactor, pixelSize, doubletId)
            if df_all is None:
                df_all = df_relion.copy()
            else:
                df_all = df_all.append(df_relion)

        tomoNo = tomoNo + 1

    # Renumber
    df_all['TomoParticleId'] = np.arange(len(df_all), dtype=np.int16) + 1
    write_star_4(df_all, 'coord_2tomo.star') 	

