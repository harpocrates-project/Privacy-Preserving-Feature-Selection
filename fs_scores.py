from Compiler.types import *
from Compiler.library import *
from Compiler import ml
from Compiler.util import is_zero, tree_reduce
from Compiler import util, mpc_math

print_float_precision(20)

class FS_SCORES():
    def __init__(self):
        pass

    def get_bound(self, Hxy0, Hxy1, Hxy2, P0, P1, P2, L0, L1, L2, feature_index, inst_len, Hy):

        temp_sum = Array(1, sfix)
        temp_sum.assign_all(0)

        @for_range_opt(inst_len)
        def _(i):
            temp_sum[0] += -(P0[i][feature_index]+P1[i][feature_index]+P2[i][feature_index])*(L0[i][feature_index] + L1[i][feature_index] + L2[i][feature_index])
        
        temp_sum[0] += -(Hxy0[feature_index]+Hxy1[feature_index]+Hxy2[feature_index])

        # temp_sum[0] += 3.1327380925458095 # correction synthbig
        # temp_sum[0] += 0.6720755444362114 # correction spambase
        # temp_sum[0] += 0.6930971797265786 # correction gisette

        temp_sum[0] += Hy

        temp_sum[0].reveal().print_plain()
        print_ln()

        return temp_sum[0]

    def get_mi(self, hjoint0, hjoint1, hjoint2, P0, P1, P2, feature_index, inst_len, Hy):

        temp_sum = Array(1, sfix)
        temp_sum.assign_all(0)

        @for_range_opt(inst_len)
        def _(i):
            temp_sum[0] += (hjoint0[i][feature_index]+hjoint1[i][feature_index]+hjoint2[i][feature_index])*mpc_math.log2_fx(hjoint0[i][feature_index]+hjoint1[i][feature_index]+hjoint2[i][feature_index])

        @for_range_opt(P0.sizes[0])
        def _(i):
            temp_sum[0] += -(P0[i][feature_index]+P1[i][feature_index]+P2[i][feature_index])*mpc_math.log2_fx(P0[i][feature_index]+P1[i][feature_index]+P2[i][feature_index])

        temp_sum[0] += Hy

        temp_sum[0].reveal().print_plain()
        print_ln()

        return temp_sum[0]

    def get_all_bounds(self, Hxy0, Hxy1, Hxy2, P0, P1, P2, L0, L1, L2, hy0, hy1, hy2):
        # start_timer(3)
        Hy = self.get_Hy(hy0, hy1, hy2)

        inst_len = L0.sizes[0]
        raw_features_len = L0.sizes[1]

        start_timer(1)
        score_arr = Array(raw_features_len,sfix)
        score_arr.assign_all(0)
        # stop_timer(3)
        @for_range_opt(raw_features_len)
        def _(i):
            # start_timer(2)
            score_arr[i] = self.get_bound(Hxy0, Hxy1, Hxy2, P0, P1, P2, L0, L1, L2, i, inst_len, Hy)
            # stop_timer(2)
        stop_timer(1)


    def get_all_mi(self, hjoint0, hjoint1, hjoint2, P0, P1, P2, hy0, hy1, hy2):
        # start_timer(3)
        Hy = self.get_Hy(hy0, hy1, hy2)

        inst_len = hjoint0.sizes[0]
        raw_features_len = hjoint0.sizes[1]

        start_timer(1)
        score_arr = Array(raw_features_len,sfix)
        score_arr.assign_all(0)
        # stop_timer(3)
        @for_range_opt(raw_features_len)
        def _(i):
            # start_timer(2)
            score_arr[i] = self.get_mi(hjoint0, hjoint1, hjoint2, P0, P1, P2, i, inst_len, Hy)
            # stop_timer(2)
        stop_timer(1)

    def get_Hy(self, hy0, hy1, hy2):

        temp_sum = Array(1, sfix)
        temp_sum.assign_all(0)

        @for_range_opt(hy0.sizes[0])
        def _(i):
            temp_sum[0] += -(hy0[i]+hy1[i]+hy2[i])*mpc_math.log2_fx(hy0[i]+hy1[i]+hy2[i])

        return temp_sum[0]
        
  