from nnmnkwii.io import hts


# Duplicated from no2.utils.util
def merge_sil(lab):
    N = len(lab)
    f = hts.HTSLabelFile()
    f.append(lab[0], strict=False)
    is_full_context = "@" in lab[0][-1]
    for i in range(1, N):
        if (is_full_context and "-sil" in f[-1][-1] and "-sil" in lab[i][-1]) or (
            not is_full_context and f[-1][-1] == "sil" and lab[i][-1] == "sil"
        ):
            # extend sil
            f.end_times[-1] = lab[i][1]
        else:
            f.append(lab[i], strict=False)
    return f
