# FS_MPC

For these scripts we use the [MP-SPDZ library](https://github.com/data61/MP-SPDZ) for secure multiparty computations. To run the scripts, you can download one of the releases of MP-SPDZ [here](https://github.com/data61/MP-SPDZ///releases) (tested with version 0.3.7).

Copy the relevant data set files from ./data to a directory mp-spdz/Player-Data in the root of MP-SPDZ (you may need to create it). Copy run.sh and data_prep.py to mp-spdz/. Also, copy fs_scores.py to mp-spdz/Compiler/ and source_file.mpc to mp-spdz/Programs/Source/.

The bash script ./run.sh will set off a 3-party computation of MI in the naive manner. You can choose data set in run.sh and also switch to computing the upper bound of MI at the end of source_file.mpc (switch to fs_scores.get_all_bounds).