import os

def create_sim_directories(path_name):
    sim_data_dir     = str(path_name)+'/sim_data'
    germline_out_dir = str(path_name)+'/germline_out'
    sim_results_dir  = str(path_name)+'/results'

    ### Check if necessary directories exist.
    dir_list = [sim_data_dir, germline_out_dir, sim_results_dir]
    for d in dir_list:
        try:
            os.makedirs(d)
        except OSError:
            if not os.path.isdir(d):
                raise
    return dir_list


def write_sim_results_file(dir, job, param_dict, res_list, header):
    result = '{}/results_{}.txt'.format(dir, job)
    out_file = open(result, 'w')

    #lines write_sims_file
    params = []
    vals = []
    for param, val in param_dict.items():
        params.append(param)
        vals.append(str(val))
    #header from write_results_file
    header = '\t'.join(header)+'\n'
    out = '\t'.join([str(r) for r in res_list]) + '\n'

    out_file.write('\t'.join(params) + '\t' + header)
    out_file.write('\t'.join(vals) + '\t' + out)


def write_stats_file(res_dir, job, res_list, header):
    header = '\t'.join(header)+'\n'
    file_dir_name = '{0}/{1}.summary'.format(res_dir, job)
    out_file  = open(file_dir_name, 'w')
    out_file.write(header)

    out = '\t'.join([str(r) for r in res_list]) + '\n'
    out_file.write(out)
    out_file.close()